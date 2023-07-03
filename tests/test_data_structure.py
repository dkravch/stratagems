import io

from stratagems.base.data_structure import Stratagems


def test_banana():

    chapter = "Test Chapter"
    name = "Do banana"
    content = "Whatever happen do banana"

    data = io.StringIO(f"# {chapter}\n"
                       f"## {name}\n"
                       f"{content}\n")

    stratagems = Stratagems(data)
    stratagems.show()
    item = stratagems.get_random_stratagem()
    assert item['chapter'] == chapter
    assert item['name'] == name
    assert item['content'] == content
