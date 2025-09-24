from flask import Flask, render_template
from pyngrok import ngrok
import threading
import requests
import os

app = Flask(__name__, template_folder='templates')  # Thay đổi vì: Rõ ràng chỉ định thư mục templates để tránh lỗi đường dẫn.
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Bật auto-reload template để tránh caching.

# Supabase configuration
SUPABASE_URL = "https://ocateixuzulwmrtxseom.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9jYXRlaXh1enVsd21ydHhzZW9tIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYyMTYyMTQsImV4cCI6MjA3MTc5MjIxNH0.w7PLqjLGj4hNNGDh81NwDodEUCCqVSVm_PL0FpYWif8"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# Home route
@app.route('/')
def home():
    response = requests.get(f"{SUPABASE_URL}/rest/v1/products?select=product_id,product_name,unit_price,units_in_stock", headers=HEADERS)
    print("API Response Status:", response.status_code)  # In trạng thái HTTP.
    print("API Response Data:", response.text)  # In dữ liệu trả về.
    if response.status_code == 200:
        products = response.json() or []  # Thay đổi vì: Đảm bảo products là list rỗng nếu JSON không hợp lệ.
        print("Products Data:", products)
        print("Number of Products:", len(products))
        print("Template Path:", os.path.join(app.template_folder, 'trangchu.html'))
        print("Template Exists:", os.path.exists(os.path.join(app.template_folder, 'trangchu.html')))  # Thay đổi vì: Kiểm tra xem file template có tồn tại không.
        return render_template('trangchu.html', products=products)
    else:
        return f"Error fetching products: {response.status_code} - {response.text}", 500

# Product detail route
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/products?product_id=eq.{product_id}&select=product_id,product_name,unit_price,units_in_stock,quantity_per_unit,units_on_order,reorder_level,discontinued",
        headers=HEADERS
    )
    print("Detail API Response Status:", response.status_code)
    print("Detail API Response Data:", response.text)
    if response.status_code == 200:
        products = response.json()
        if products:
            return render_template('product_detail.html', product=products[0])
        else:
            return "Product not found", 404
    else:
        return f"Error fetching product details: {response.status_code} - {response.text}", 500

# Subpage routes
@app.route('/gioi-thieu')
def gioi_thieu():
    return render_template('gioi_thieu.html')

@app.route('/chuong-trinh-hoc')
def chuong_trinh_hoc():
    return render_template('chuong_trinh_hoc.html')

@app.route('/trai-nghiem-sinh-vien')
def trai_nghiem_sinh_vien():
    return render_template('trai_nghiem_sinh_vien.html')

@app.route('/goc-truyen-thong')
def goc_truyen_thong():
    return render_template('goc_truyen_thong.html')

@app.route('/doanh-nghiep')
def doanh_nghiep():
    return render_template('doanh_nghiep.html')

@app.route('/lien-he')
def lien_he():
    return render_template('lien_he.html')

def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    ngrok.kill()  # Đóng tất cả tunnel hiện tại để tránh lỗi ERR_NGROK_324.
    public_url = ngrok.connect(5000).public_url
    print(f" * ngrok tunnel available at: {public_url}")
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()