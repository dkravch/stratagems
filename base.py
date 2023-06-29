import json
import random

import markdown_to_json


class Strategems:

    def __init__(self):
        with open("36.md") as f:
            markdown_file_content = f.read()
        jsonified = markdown_to_json.jsonify(markdown_file_content)
        self.strategem_dict = json.loads(jsonified)

    def show(self):
        for chapter_name, chapter_content in self.strategem_dict.items():
            print(chapter_name.upper())
            for name, value in chapter_content.items():
                print(f">>> {name}")
                print(f"{value}")

    def get_random_strategem(self):
        chapter = random.choice(list(self.strategem_dict.keys()))
        name = random.choice(list(self.strategem_dict[chapter].keys()))
        content = self.strategem_dict[chapter][name]
        return dict(chapter=chapter,
                    name=name,
                    content=content)


if __name__ == '__main__':
    s = Strategems()
    s.show()
    print("="*80)
    print(s.get_random_strategem())