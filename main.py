import tkinter as tk
from tkinter import messagebox
import webbrowser
import scrapy
from scrapy.crawler import CrawlerProcess
import threading
import csv
from autocorrect import Speller
from PIL import Image, ImageTk
import requests
from io import BytesIO

spell = Speller()

class GiftyAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gifty.ai - Your Personalized Gift Finder")
        self.root.geometry("800x600")  # Set initial window size
        self.root.resizable(True, True)  # Allow resizing
        
        self.questions = [
            "Who is the gift for?",
            "What is the occasion?",
            "What are their interests?",
            "What is their age?",
            "Do they prefer practical or sentimental gifts?",
            "Do they have any specific hobbies or any favorite brands on amazon?",
            "What is your budget?",
            "Do they have any dislikes?"
        ]
        
        self.answers = {}
        self.current_question = 0
        
        self.label = tk.Label(root, text=self.questions[self.current_question], font=("Arial", 16, "bold"), bg="#f0f0f0")
        self.label.pack(pady=20)
        
        self.entry = tk.Entry(root, font=("Arial", 14), width=50)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", lambda event: self.next_question())
        
        self.button_frame = tk.Frame(root, bg="#f0f0f0")
        self.button_frame.pack()
        
        self.next_button = tk.Button(self.button_frame, text="Next", command=self.next_question, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", padx=20, pady=5)
        self.next_button.pack(side=tk.LEFT, padx=10)
        
        self.feedback_label = tk.Label(root, text="", font=("Arial", 14), bg="#f0f0f0")
        self.feedback_label.pack()
    
    def next_question(self):
        answer = self.entry.get().strip()
        answer = spell(answer) if answer else "Skipped"
        
        self.answers[self.questions[self.current_question]] = answer
        self.entry.delete(0, tk.END)
        
        self.current_question += 1
        
        if self.current_question < len(self.questions):
            self.label.config(text=self.questions[self.current_question])
        else:
            self.save_answers()
            self.label.config(text="Finding the perfect gift...")
            self.entry.pack_forget()
            self.next_button.pack_forget()
            self.start_scraping()
    
    def save_answers(self):
        with open("responses.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.answers.values())
    
    def start_scraping(self):
        thread = threading.Thread(target=self.run_scraper)
        thread.start()
    
    def run_scraper(self):
        process = CrawlerProcess()
        process.crawl(GiftSpider, answers=self.answers, app=self)
        process.start()
    
    def display_results(self, products):
        self.label.config(text="Here are the best gift options:")
        
        # Create a frame for the results
        self.results_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.results_frame.pack(fill="both", expand=True)
        
        # Create a canvas for the results
        self.canvas = tk.Canvas(self.results_frame, bg="#f0f0f0")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create a scrollbar for the results
        self.scrollbar = tk.Scrollbar(self.results_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        # Configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create a frame for the products
        self.products_frame = tk.Frame(self.canvas, bg="#f0f0f0")
        self.canvas.create_window((0, 0), window=self.products_frame, anchor="center")  # Center the products
        
        # Display the products
        for product in products[:3]:  # Ensure we only display up to 3 products
            frame = tk.Frame(self.products_frame, bg="#ffffff", padx=10, pady=10, bd=2, relief=tk.RIDGE)
            frame.pack(pady=5, fill=tk.X)
            
            tk.Label(frame, text=product['title'], font=("Arial", 14, "bold"), bg="#ffffff").pack(anchor="w")
            tk.Label(frame, text=f"Price: ₹{product['price']}", font=("Arial", 12), bg="#ffffff").pack(anchor="w")
            
            if product['image']:
                try:
                    # Fetch the image
                    response = requests.get(product['image'])
                    img_data = BytesIO(response.content)
                    img = Image.open(img_data)
                    img = img.resize((150, 150))  # Resize image to fit
                    img_tk = ImageTk.PhotoImage(img)
                    
                    image_label = tk.Label(frame, image=img_tk, bg="#ffffff")
                    image_label.image = img_tk  # Keep a reference to avoid garbage collection
                    image_label.pack(anchor="w")
                except Exception as e:
                    print(f"Error loading image: {e}")
            
            if product['link']:
                link = tk.Label(frame, text="Buy Now", fg="blue", cursor="hand2", font=("Arial", 12, "underline"), bg="#ffffff")
                link.pack(anchor="w")
                link.bind("<Button-1>", lambda e, url=product['link']: webbrowser.open(url))
        
        self.add_feedback_section()
        
        # Update the scroll region of the canvas
        self.products_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
        # Bind mouse wheel scrolling
        self.root.bind_all("<MouseWheel>", self.on_mouse_wheel)
    
    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def add_feedback_section(self):
        self.feedback_label.config(text="Did you find this helpful?")
        self.feedback_entry = tk.Entry(self.root, font=("Arial", 14), width=50)
        self.feedback_entry.pack(pady=10)
        
        self.feedback_button = tk.Button(self.root, text="Submit Feedback", command=self.save_feedback, font=("Arial", 12, "bold"), bg="#008CBA", fg="white", padx=20, pady=5)
        self.feedback_button.pack()
    
    def save_feedback(self):
        feedback = self.feedback_entry.get()
        with open("feedback.txt", "a") as file:
            file.write(feedback + "\n")
        messagebox.showinfo("Thank you!", "Your feedback has been recorded.")
        self.feedback_entry.delete(0, tk.END)

class GiftSpider(scrapy.Spider):
    name = "gift_spider"
    
    def __init__(self, answers, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.answers = answers
        self.app = app
        self.start_urls = [f"https://www.amazon.in/s?k={answers['Who is the gift for?']}+{answers['What is the occasion?']}+{answers['What are their interests?']}+{answers['What is their age group?']}+gift"]
    
    def parse(self, response):
        products = []
        for item in response.css(".s-main-slot .s-result-item")[:5]:
            title = item.css(".a-text-normal::text").get()
            price = item.css(".a-price-whole::text").get(default="Unknown")
            link = response.urljoin(item.css(".a-link-normal::attr(href)").get())
            image = item.css(".s-image::attr(src)").get()
            
            if title and price and link and image:
                products.append({"title": title, "price": price, "link": link, "image": image})
        
        while len(products) < 3:
            products.append({"title": "Alternative Gift", "price": "Unknown", "link": "", "image": ""})
        
        self.app.display_results(products)

if __name__ == "__main__":
    root = tk.Tk()
    app = GiftyAIApp(root)
    root.mainloop()