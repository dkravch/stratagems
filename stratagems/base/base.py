import json
import random

import markdown_to_json


class Stratagems:

    def __init__(self, stratagem_file_path=None):
        with open(stratagem_file_path) as f:
            markdown_file_content = f.read()
        jsonified = markdown_to_json.jsonify(markdown_file_content)
        self.stratagem_dict = json.loads(jsonified)

    def show(self):
        for chapter_name, chapter_content in self.stratagem_dict.items():
            print(chapter_name.upper())
            for name, value in chapter_content.items():
                print(f">>> {name}")
                print(f"{value}")

    def get_random_stratagem(self):
        chapter = random.choice(list(self.stratagem_dict.keys()))
        name = random.choice(list(self.stratagem_dict[chapter].keys()))
        content = self.stratagem_dict[chapter][name]
        return dict(chapter=chapter,
                    name=name,
                    content=content)


if __name__ == '__main__':
    s = Stratagems()
    s.show()
    print("="*80)
    print(s.get_random_stratagem())
