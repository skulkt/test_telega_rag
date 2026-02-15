import re
import pandas as pd

from io import BytesIO

from langchain_core.documents import Document


# Это хардкод, а что поделать
class TextProcessor:
    def process(self, text: str) -> list[dict]:
        first_line = text.split("\n")[0].strip()

        if "О Якутии" in first_line:
            content = "\n".join(text.split("\n")[1:]).strip()
            return [{"category": "about", "content": content}]
        elif "Музеи" in first_line:
            return self._parse_new_line(text, "museums")
        elif "Рестораны" in first_line:
            return self._parse_restaurants(text, "restaurants")
        elif "Мероприятия" in first_line:
            return self._parse_double_new_line(text, "events")
        elif "Гостиницы" in first_line:
            return self._parse_simple_list(text, "hotels")
        elif "Сувениры" in first_line:
            return self._parse_simple_list(text, "gifts")
        else:
            return []

    def _parse_new_line(self, text: str, category: str):
        items = re.split(r"\n", text)
        return self._make_result(items, category)

    def _parse_double_new_line(self, text: str, category: str):
        items = re.split(r"\n\n", text)
        return self._make_result(items, category)

    def _parse_simple_list(self, text: str, category: str):
        items = re.split(r"\n(?=\d+\.\s)", text)
        return self._make_result(items, category)

    def _parse_restaurants(self, text: str, category: str):
        items = re.split(r'\n(?=[«"])', text)
        return self._make_result(items, category)

    def _parse_events(self, text: str, category: str):
        items = re.split(r"\n(?=[А-ЯЁ][а-яё]+\s+[а-яё]+\n)", text)
        return self._make_result(items, category)

    def _make_result(self, items: list[str], category: str):
        result = []
        letters_count = 5

        for item in items:
            clean_item = item.strip()

            if len(clean_item) > letters_count and not clean_item.endswith(":"):
                result.append({"category": category, "content": clean_item})

        return result


class ExcelDataParser:
    def __init__(
        self,
    ):
        self.text_processor = TextProcessor()

    def parse(self, file_bytes: bytes) -> list[Document]:
        file = BytesIO(file_bytes)
        df = pd.read_excel(io=file)
        data = []
        documents = []

        for _, row in df.iterrows():
            content = str(row.iloc[0])
            data.extend(self.text_processor.process(content))

        for item in data:
            documents.append(
                Document(
                    page_content=item["content"],
                    metadata={
                        "category": item["category"],
                    },
                )
            )

        return documents
