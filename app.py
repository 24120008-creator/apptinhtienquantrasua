import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
import random

# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Smart Milk Tea Shop",
    page_icon="🧋",
    layout="wide"
)

# =========================================================
# CSS - THIẾT KẾ GIAO DIỆN
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #fff8fb;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #d63384;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    color: #777;
    font-size: 18px;
    margin-bottom: 25px;
}

.card {
    padding: 20px;
    border-radius: 18px;
    background-color: white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.total-box {
    padding: 20px;
    border-radius: 18px;
    background-color: #fff0f6;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    color: #d63384;
}

.chat-box {
    padding: 15px;
    border-radius: 15px;
    background-color: #f8f9fa;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DỮ LIỆU MENU
# =========================================================

MENU = {
    "Trà sữa truyền thống": {
        "price": 30000,
        "image": "images/truyen_thong.jpg"
    },
    "Trà sữa trân châu đường đen": {
        "price": 35000,
        "image": "images/duong_den.jpg"
    },
    "Trà đào": {
        "price": 28000,
        "image": "images/tra_dao.jpg"
    },
    "Trà vải": {
        "price": 28000,
        "image": "images/tra_vai.jpg"
    },
    "Matcha Latte": {
        "price": 42000,
        "image": "images/matcha.jpg"
    }
}

SIZE_PRICE = {
    "S": 0,
    "M": 5000,
    "L": 10000
}

TOPPING_PRICE = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 7000,
    "Pudding": 8000
}

SUGAR_LEVEL = [
    "100%",
    "70%",
    "50%",
    "0%"
]

ICE_LEVEL = [
    "Đá bình thường",
    "Ít đá",
    "Không đá"
]

# =========================================================
# SESSION STATE
# =========================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "orders" not in st.session_state:
    st.session_state.orders = []

# =========================================================
# HEADER
# =========================================================

try:
    st.image("images/logo.jpg", width=180)
except:
    pass

st.markdown(
    '<div class="title">🧋 SMART MILK TEA SHOP</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Mini App quản lý bán hàng thông minh</div>',
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📌 MENU")

page = st.sidebar.radio(
    "Chọn chức năng",
    [
        "🏠 Đặt hàng",
        "🧾 Hóa đơn",
        "🤖 Chatbot AI",
        "📊 Doanh thu"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "📍 1119B Đại lộ Bình Dương\n\n"
    "🕐 08:00 - 22:00\n\n"
    "☎️ Hotline: 0900 000 000"
)

# =========================================================
# TRANG ĐẶT HÀNG
# =========================================================

if page == "🏠 Đặt hàng":

    st.header("🛒 Đặt món")

    col1, col2 = st.columns([1, 1])

    with col1:

        st.subheader("👤 Thông tin khách hàng")

        customer_name = st.text_input(
            "Tên khách hàng",
            placeholder="Nhập tên..."
        )

        customer_phone = st.text_input(
            "Số điện thoại",
            placeholder="Nhập số điện thoại..."
        )

        st.markdown("---")

        st.subheader("🥤 Chọn món")

        selected_drink = st.selectbox(
            "Món uống",
            list(MENU.keys())
        )

        # Hiển thị hình món
        image_path = MENU[selected_drink]["image"]

        try:
            st.image(
                image_path,
                caption=selected_drink,
                width=250
            )
        except:
            st.info("Chưa có hình món này.")

        base_price = MENU[selected_drink]["price"]

        size = st.selectbox(
            "📏 Size",
            list(SIZE_PRICE.keys())
        )

        topping = st.selectbox(
            "🍮 Topping",
            list(TOPPING_PRICE.keys())
        )

        sugar = st.select_slider(
            "🍬 Độ ngọt",
            options=SUGAR_LEVEL,
            value="70%"
        )

        ice = st.selectbox(
            "🧊 Lượng đá",
            ICE_LEVEL
        )

        quantity = st.number_input(
            "🔢 Số lượng",
            min_value=1,
            max_value=20,
            value=1,
            step=1
        )

        item_price = (
            base_price
            + SIZE_PRICE[size]
            + TOPPING_PRICE[topping]
        )

        item_total = item_price * quantity

        st.info(
            f"Đơn giá: {item_price:,.0f} VNĐ\n\n"
            f"Thành tiền: {item_total:,.0f} VNĐ"
        )

        if st.button(
            "➕ THÊM VÀO GIỎ",
            use_container_width=True
        ):

            item = {
                "Món": selected_drink,
                "Size": size,
                "Topping": topping,
                "Đường": sugar,
                "Đá": ice,
                "Số lượng": quantity,
                "Đơn giá": item_price,
                "Thành tiền": item_total
            }

            st.session_state.cart.append(item)

            st.success(
                f"Đã thêm {selected_drink} vào giỏ!"
            )

    # =====================================================
    # GIỎ HÀNG
    # =====================================================

    with col2:

        st.subheader("🛒 Giỏ hàng")

        if len(st.session_state.cart) == 0:

            st.info(
                "Giỏ hàng đang trống. "
                "Hãy chọn món và thêm vào giỏ."
            )

        else:

            for i, item in enumerate(
                st.session_state.cart
            ):

                st.markdown(
                    f"""
                    *{i+1}. {item['Món']}*

                    Size: {item['Size']} | 
                    Topping: {item['Topping']}  

                    Đường: {item['Đường']} | 
                    {item['Đá']}  

                    Số lượng: {item['Số lượng']}  

                    Thành tiền: 
                    *{item['Thành tiền']:,.0f} VNĐ*
                    """
                )

                if st.button(
                    f"❌ Xóa món {i+1}",
                    key=f"delete_{i}"
                ):

                    st.session_state.cart.pop(i)

                    st.rerun()

                st.markdown("---")

            subtotal = sum(
                item["Thành tiền"]
                for item in st.session_state.cart
            )

            # =============================================
            # GIẢM GIÁ
            # =============================================

            discount_percent = st.selectbox(
                "🎁 Khuyến mãi",
                [0, 5, 10, 15]
            )

            discount = subtotal * discount_percent / 100

            total = subtotal - discount

            st.markdown(
                f"""
                <div class="total-box">
                💰 TỔNG THANH TOÁN<br>
                {total:,.0f} VNĐ
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("### 💳 Phương thức thanh toán")

            payment = st.radio(
                "Chọn phương thức",
                [
                    "💵 Tiền mặt",
                    "🏦 Chuyển khoản",
                    "💳 Thẻ ngân hàng"
                ]
            )

            # =============================================
            # THANH TOÁN
            # =============================================

            if st.button(
                "✅ THANH TOÁN",
                use_container_width=True
            ):

                if not customer_name:

                    st.warning(
                        "Vui lòng nhập tên khách hàng!"
                    )

                else:

                    order = {
                        "Thời gian":
                            datetime.now().strftime(
                                "%d/%m/%Y %H:%M"
                            ),

                        "Khách hàng":
                            customer_name,

                        "Số điện thoại":
                            customer_phone,

                        "Số món":
                            len(st.session_state.cart),

                        "Tổng tiền":
                            total,

                        "Thanh toán":
                            payment
                    }

                    st.session_state.orders.append(
                        order
                    )

                    st.session_state.last_order = {
                        "customer": customer_name,
                        "phone": customer_phone,
                        "items": st.session_state.cart.copy(),
                        "subtotal": subtotal,
                        "discount": discount,
                        "discount_percent":
                            discount_percent,
                        "total": total,
                        "payment": payment,
                        "time":
                            datetime.now().strftime(
                                "%d/%m/%Y %H:%M:%S"
                            )
                    }

                    st.session_state.cart = []

                    st.success(
                        "🎉 Thanh toán thành công!"
                    )

                    st.balloons()

# =========================================================
# TRANG HÓA ĐƠN
# =========================================================

elif page == "🧾 Hóa đơn":

    st.header("🧾 Hóa đơn")

    if "last_order" not in st.session_state:

        st.info(
            "Chưa có hóa đơn. "
            "Vui lòng đặt hàng trước."
        )

    else:

        order = st.session_state.last_order

        invoice = ""

        invoice += (
            "====================================\n"
        )
        invoice += (
            "       🧋 SMART MILK TEA SHOP\n"
        )
        invoice += (
            "       1119B ĐẠI LỘ BÌNH DƯƠNG\n"
        )
        invoice += (
            "====================================\n"
        )

        invoice += (
            f"Khách hàng: {order['customer']}\n"
        )

        invoice += (
            f"SĐT: {order['phone']}\n"
        )

        invoice += (
            f"Thời gian: {order['time']}\n"
        )

        invoice += (
            "------------------------------------\n"
        )

        for i, item in enumerate(
            order["items"], 1
        ):

            invoice += (
                f"{i}. {item['Món']}\n"
            )

            invoice += (
                f"   Size: {item['Size']}\n"
            )

            invoice += (
                f"   Topping: {item['Topping']}\n"
            )

            invoice += (
                f"   Đường: {item['Đường']}\n"
            )

            invoice += (
                f"   Đá: {item['Đá']}\n"
            )

            invoice += (
                f"   SL: {item['Số lượng']}\n"
            )

            invoice += (
                f"   Thành tiền: "
                f"{item['Thành tiền']:,.0f} VNĐ\n"
            )

        invoice += (
            "------------------------------------\n"
        )

        invoice += (
            f"Tạm tính: "
            f"{order['subtotal']:,.0f} VNĐ\n"
        )

        invoice += (
            f"Giảm giá: "
            f"{order['discount']:,.0f} VNĐ\n"
        )

        invoice += (
            f"TỔNG TIỀN: "
            f"{order['total']:,.0f} VNĐ\n"
        )

        invoice += (
            f"Thanh toán: "
            f"{order['payment']}\n"
        )

        invoice += (
            "====================================\n"
        )

        invoice += (
            "       CẢM ƠN QUÝ KHÁCH! ❤️\n"
        )

        st.code(
            invoice,
            language="text"
        )

        st.download_button(
            "📥 TẢI HÓA ĐƠN",
            data=invoice,
            file_name="hoa_don_milk_tea.txt",
            mime="text/plain",
            use_container_width=True
        )

# =========================================================
# CHATBOT
# =========================================================

elif page == "🤖 Chatbot AI":

    st.header("🤖 Chatbot tư vấn đồ uống")

    st.markdown(
        """
        <div class="chat-box">
        👋 Xin chào! Mình là trợ lý của
        Smart Milk Tea Shop.
        <br><br>
        Bạn có thể hỏi:
        <br>
        • Món nào ngon?
        <br>
        • Món nào ít ngọt?
        <br>
        • Món nào có matcha?
        <br>
        • Món nào dưới 30.000đ?
        </div>
        """,
        unsafe_allow_html=True
    )

    question = st.text_input(
        "💬 Nhập câu hỏi..."
    )

    if question:

        q = question.lower()

        if (
            "ngon" in q
            or "gợi ý" in q
        ):

            st.success(
                "🧋 Mình gợi ý "
                "Trà sữa trân châu đường đen. "
                "Đây là một trong những món "
                "dễ uống và được nhiều khách yêu thích!"
            )

        elif (
            "ít ngọt" in q
            or "không ngọt" in q
        ):

            st.success(
                "🍑 Bạn có thể chọn Trà đào "
                "với mức đường 0% hoặc 50%."
            )

        elif "matcha" in q:

            st.success(
                "🍵 Matcha Latte có giá "
                "42.000 VNĐ. "
                "Bạn có thể chọn size M hoặc L."
            )

        elif (
            "30" in q
            or "30000" in q
        ):

            st.success(
                "💰 Các món khoảng 30.000 VNĐ "
                "gồm Trà đào, Trà vải và "
                "Trà sữa truyền thống."
            )

        elif "giảm cân" in q:

            st.success(
                "🥰 Nếu bạn muốn uống nhẹ hơn, "
                "hãy chọn Trà đào hoặc Trà vải, "
                "50% hoặc 0% đường và ít đá."
            )

        else:

            st.info(
                "🤖 Bạn có thể hỏi mình về "
                "món uống, giá tiền, độ ngọt "
                "hoặc món phù hợp với bạn nhé!"
            )

# =========================================================
# TRANG DOANH THU
# =========================================================

elif page == "📊 Doanh thu":

    st.header("📊 Thống kê bán hàng")

    if len(st.session_state.orders) == 0:

        st.info(
            "Chưa có dữ liệu doanh thu. "
            "Hãy tạo đơn hàng trước."
        )

    else:

        df = pd.DataFrame(
            st.session_state.orders
        )

        total_revenue = df["Tổng tiền"].sum()

        total_orders = len(df)

        average_order = (
            total_revenue / total_orders
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "💰 Tổng doanh thu",
                f"{total_revenue:,.0f} VNĐ"
            )

        with col2:

            st.metric(
                "🧾 Số đơn hàng",
                total_orders
            )

        with col3:

            st.metric(
                "📈 Giá trị đơn TB",
                f"{average_order:,.0f} VNĐ"
            )

        st.subheader(
            "📋 Danh sách đơn hàng"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        st.subheader(
            "📈 Biểu đồ doanh thu"
        )

        chart_data = df[
            ["Thời gian", "Tổng tiền"]
        ].copy()

        chart_data = chart_data.set_index(
            "Thời gian"
        )

        st.bar_chart(
            chart_data
        )

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <center>
    🧋 <b>SMART MILK TEA SHOP</b><br>
    Mini App quản lý bán hàng<br>
    © 2026
    </center>
    """,
    unsafe_allow_html=True
)
Soạn
Viết cho Nguyễn Minh Thư


