import planetary_computer
import pystac_client
import rasterio
from rasterio.plot import show

# 連接 Planetary Computer STAC API
catalog = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")

# 搜索 Sentinel-2 遙感影像
search = catalog.search(
    collections=["sentinel-2-l2a"],
    bbox=[-122.5, 37.5, -122.0, 38.0],  # 設定地理範圍 (舊金山)
    datetime="2023-01-01/2023-12-31",
)

# 取得影像
items = list(search.items())
if items:
    item = items[0]
    signed_asset = planetary_computer.sign(item.assets["B04"]).href  # 取得紅光波段影像

    # 讀取影像並顯示
    with rasterio.open(signed_asset) as dataset:
        show(dataset)
    dataset.read(1).tofile("output_image.tif")  # 儲存影像

else:
    print("未找到符合條件的數據")
