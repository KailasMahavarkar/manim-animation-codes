import json

canvas = {
    "nodes": [
        {"id": "26b89010b3cd7a24", "type": "text", "text": "1338. Reduce Array Size to The Half",
            "x": -531, "y": -282, "width": 361, "height": 60, "color": "2"},
        {"id": "09326b6d0f1f6a73", "type": "text", "text": "1094. Car Pooling",
         "x": -531, "y": -160, "width": 361, "height": 60, "color": "2"}
    ],
    "edges": []
}


def question_to_link(str):
    if len(str.split(".")) != 2:
        return str

    problem_number = str.split(".")[0]
    question = str.split(".")[1]

    dynamic = question.replace(' ', '-').lower()
    if dynamic[0] == '-':
        dynamic = dynamic[1:]

    link = f"https://leetcode.com/problems/{dynamic}/description/"
    return link


# Iterate over the nodes and convert the text into the desired format
for node in canvas["nodes"]:
    question = node["text"]
    link = question_to_link(question)
    node["text"] = f"[{question}]({link})"

print(json.dumps(canvas, indent=2))
