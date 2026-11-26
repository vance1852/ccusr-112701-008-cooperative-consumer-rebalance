"""读取原始数据清册和端点记录。"""

import argparse
import json
from pathlib import Path


def inventory(directory):
    result = json.loads((directory / "inventory.json").read_text("utf-8"))
    if not isinstance(result, dict) or not result:
        raise ValueError("清册须为非空对象")
    return result


def observations(path):
    previous = 0
    with path.open(encoding="utf-8") as source:
        for number, line in enumerate(source, 1):
            try:
                event = json.loads(line)
                if not isinstance(event, dict) or type(event.get("at")) is not int or event["at"] < previous:
                    raise ValueError("缺少整数接收时钟或顺序错误")
                if not isinstance(event.get("kind"), str) or not event["kind"]:
                    raise ValueError("缺少事件类别")
            except ValueError as error:
                raise ValueError(f"{path.name}:{number} {error}") from error
            previous = event["at"]
            yield event


def main():
    parser = argparse.ArgumentParser(description="读取合成业务观察")
    parser.add_argument("source", type=Path)
    parser.add_argument("--kind", help="按事件类别筛选")
    args = parser.parse_args()
    try:
        inventory(args.source.parent)
        for item in observations(args.source):
            if args.kind is None or item["kind"] == args.kind:
                print(json.dumps(item, ensure_ascii=False))
    except (OSError, ValueError) as error:
        parser.exit(2, f"资料有误：{error}\n")


if __name__ == "__main__":
    main()
