import json

import scrapy
from scrapy.http import Response


# class McdonaldsSpider(scrapy.Spider):
#     name = "mcdonalds"
#     allowed_domains = ["www.mcdonalds.com"]
#     start_urls = ["https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html"]
#
#     def parse_item(self, response: Response):
#         og_url = response.css("meta[property='og:url']::attr(content)").get()
#         id_item = og_url.split("/")[-1].replace(".html", "") if og_url else "Н/Д"
#         yield{
#             "title": response.css(".cmp-product-details-main__heading-title::text").get(),
#             "description": " ".join(response.css("div.cmp-product-details-main__description *::text").getall()).strip(),
#             "id_item": id_item
#
#         }
#
#     def parse(self, response: Response, **kwargs):
#
#         for item in response.css("li.cmp-category__item"):
#             item_link = response.urljoin(item.css("a.cmp-category__item-link::attr(href)").get())
#             yield scrapy.Request(item_link, callback=self.parse_item)


class McDonaldsLinkSpider(scrapy.Spider):
    name = 'mcdonalds'
    allowed_domains = ["www.mcdonalds.com"]
    start_urls = ["https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html"]

    def parse(self, response: Response, **kwargs):

        product_elements = response.css("li.cmp-category__item[data-product-id]")

        product_ids = product_elements.css("::attr(data-product-id)").getall()

        self.log(f"Found {len(product_ids)} items: {product_ids}")

        for product_id in product_ids:
            api_url = f"https://www.mcdonalds.com/dnaapp/itemDetails?country=UA&language=uk&showLiveData=true&item={product_id}"
            yield scrapy.Request(api_url, callback=self.parse_item, meta={"product_id": product_id})

    def parse_item(self, response):
        description = "N/A"
        try:
            product_data = response.json()
            item_data = product_data.get("item", {})

            nutrients = item_data.get("nutrient_facts", {}).get("nutrient", [])

            def get_nutrient_value(name):
                for nutrient in nutrients:
                    if nutrient.get("name", "").lower() == name.lower():
                        return nutrient.get("value", "N/A")
                return "N/A"

            if not isinstance(item_data.get("description", "N/A"), str):
                description = "N/A"
            else:
                description = item_data.get("description", "N/A")
            yield {
                "id": response.meta["product_id"],
                "name": item_data.get("item_name", "N/A"),
                "description": description,
                "calories": get_nutrient_value("Калорійність"),
                "fats": get_nutrient_value("Жири"),
                "carbs": get_nutrient_value("Вуглеводи"),
                "proteins": get_nutrient_value("Білки"),
                "unsaturated_fats": get_nutrient_value("НЖК"),
                "sugar": get_nutrient_value("Цукор"),
                "salt": get_nutrient_value("Сіль"),
                "portion": get_nutrient_value("Вага порції")
            }
        except Exception as e:
            self.log(f"Product processing error: {response.meta['product_id']}. Detail: {e}")