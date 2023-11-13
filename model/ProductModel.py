from sqlalchemy import Column, Float, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, MEDIUMTEXT, TINYINT
from model.BaseModel import BaseModel


class ProductModel(BaseModel):
    __tablename__ = "products"

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(200), nullable=False, index=True)  # 名称
    added_by = Column(String(6), nullable=False, server_default=text("'admin'"))
    user_id = Column(INTEGER(11), nullable=False, default=9)
    category_id = Column(INTEGER(11), nullable=False)  # 分类ID
    brand_id = Column(INTEGER(11))
    photos = Column(String(2000))  # 图片ID，格式："1,2,3"
    thumbnail_img = Column(String(100))  # 缩略图ID
    video_provider = Column(String(20), default="youtube")
    video_link = Column(String(100))
    tags = Column(String(500), index=True)
    description = Column(LONGTEXT)  # 详情，默认后几张图片
    unit_price = Column(Float(20, True), nullable=False, index=True)  # 单价
    purchase_price = Column(Float(20, True))
    variant_product = Column(INTEGER(11), nullable=False, server_default=text("0"))
    attributes = Column(String(1000), nullable=False, server_default=text("'[]'"))
    choice_options = Column(MEDIUMTEXT, default="[]")
    colors = Column(MEDIUMTEXT, default="[]")
    variations = Column(Text)
    todays_deal = Column(INTEGER(11), nullable=False, server_default=text("0"))
    published = Column(INTEGER(11), nullable=False, server_default=text("1"))
    approved = Column(TINYINT(1), nullable=False, server_default=text("1"))
    stock_visibility_state = Column(String(10), nullable=False, server_default=text("'quantity'"))
    cash_on_delivery = Column(TINYINT(1), nullable=False, server_default=text("0"), comment='1 = On, 0 = Off', default=1)
    featured = Column(INTEGER(11), nullable=False, server_default=text("0"))
    seller_featured = Column(INTEGER(11), nullable=False, server_default=text("0"))
    current_stock = Column(INTEGER(11), nullable=False, server_default=text("0"))
    unit = Column(String(20), default="Pc")
    min_qty = Column(INTEGER(11), nullable=False, server_default=text("1"))
    low_stock_quantity = Column(INTEGER(11), default=1)
    discount = Column(Float(20, True), default=0.0)
    discount_type = Column(String(10), default="amount")
    discount_start_date = Column(INTEGER(11))
    discount_end_date = Column(INTEGER(11))
    tax = Column(Float(20, True))
    tax_type = Column(String(10))
    shipping_type = Column(String(20), server_default=text("'flat_rate'"), default="free")
    shipping_cost = Column(Float(20, True), nullable=False, server_default=text("0.00"))
    is_quantity_multiplied = Column(TINYINT(1), nullable=False, server_default=text("0"), comment='1 = Mutiplied with shipping cost')
    est_shipping_days = Column(INTEGER(11))
    num_of_sale = Column(INTEGER(11), nullable=False, server_default=text("0"))
    meta_title = Column(MEDIUMTEXT)
    meta_description = Column(LONGTEXT)
    meta_img = Column(String(255), default="570")
    pdf = Column(String(255))
    slug = Column(MEDIUMTEXT, nullable=False, default="2085037198-pZxHa")
    earn_point = Column(Float(8, True), nullable=False, server_default=text("0.00"))
    refundable = Column(INTEGER(11), nullable=False, server_default=text("0"), default=1)
    rating = Column(Float(8, True), nullable=False, server_default=text("0.00"))
    barcode = Column(String(255))
    digital = Column(INTEGER(11), nullable=False, server_default=text("0"))
    auction_product = Column(INTEGER(11), nullable=False, server_default=text("0"))
    file_name = Column(String(255))
    file_path = Column(String(255))
    external_link = Column(String(500))
    external_link_btn = Column(String(255), server_default=text("'Buy Now'"))
    wholesale_product = Column(INTEGER(11), nullable=False, server_default=text("0"))
    original_id = Column(INTEGER(11), comment='Original item id copied from product warehouse')
    in_storehouse = Column(TINYINT(1), index=True, server_default=text("0"), comment='1 = In, 0 = Not In')
    created_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp()"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))
    seller_spread_package_payment_id = Column(INTEGER(11), nullable=False, comment='购买推广套餐id', default=0)
    source = Column(String(500), nullable=False, server_default=text("'lazada'"), comment='采集商品的来源 alibaba 和 lazada')
