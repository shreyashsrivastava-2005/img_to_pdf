import tkinter as tk
from tkinter import filedialog 
from reportlab.pdfgen import canvas
from PIL import Image
import os


# creating the variables
class imageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.image_paths = []
        self.output_pdf_name = tk.StringVar()
        self.selected_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        
        self.initialize_ui()
    
    def initialize_ui(self):
        title_label = tk.Label(self.root, text='Image to PDF Converter', font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)
        
        select_images_button = tk.Button(self.root, text='Select images', command = self.select_images)
        select_images_button.pack(pady=(0, 10))
        
        self.selected_images_listbox.pack(pady=(0,10), fill=tk.BOTH, expand=True)
        
        label = tk.Label(self.root, text = "Please enter the pdf name")
        label.pack()
        
        pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, width = 40, justify = 'center')
        pdf_name_entry.pack()
        
        convert_button = tk.Button(self.root, text='Click to convert', command = self.convert_images_to_pdf)
        convert_button.pack(pady=(20, 40))
        
    def select_images(self):
        self.image_paths = filedialog.askopenfilenames(title="Select images", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.update_selected_images_listbox()
        
    def update_selected_images_listbox(self):
        self.selected_images_listbox.delete(0, tk.END)
        for image_path in self.image_paths:
            _,image_path = os.path.split(image_path)
            self.selected_images_listbox.insert(tk.END,image_path)
            
    def convert_images_to_pdf(self):
        if not self.image_paths:
            return
        
        output_pdf_path = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else "output.pdf"
        pdf = canvas.Canvas(output_pdf_path, pagesize=(612, 792))
        
        for image_path in self.image_paths:
            img = Image.open(image_path)
            available_width = 540
            available_height = 720
            scale_factor = min(available_width/img.width, available_height/img.height)
            new_width = img.width*scale_factor
            new_height = img.height*scale_factor
            x_centred = (612-new_width)/2
            y_centred = (792-new_height)/2
            
            pdf.setFillColorRGB(255, 255, 255)
            pdf.rect(0, 0, 612, 792, fill=True)
            pdf.drawInlineImage(image_path,x_centred,y_centred, width = new_width, height=new_height)
            pdf.showPage()
            
        pdf.save()
        
        
def main():
    root = tk.Tk()
    root.title("Image to PDF Converter")
    converter = imageToPDFConverter(root)
    root.geometry("400x600")
    root.mainloop()
    
if __name__ == "__main__":
    main()