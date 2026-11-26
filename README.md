# 消费组局部重平衡与输出游标原子兑现

项目使用合成清册和本地端点观察。两份记录彼此独立，各自从相同初始清册开始。记录中的请求可以未获准。来源也可能在之后才报告真实效果。

## 资料

`examples/inventory.json` 保存已知端点和契约。`examples/shift.jsonl` 与 `examples/contrast.jsonl` 每行一个 JSON 对象。`at` 是观察进入值班端的相对秒数，同一秒内维持原顺序。`kind` 标明记录来源。业务生效时间以事件自己的版本、范围和观测为准。

entries 按 partition/offset 标识。接收方 result 的 committed 代表该批业务结果和 next_offset 已共同持久化。fence 是输出端已拒绝旧 epoch 的证明；lost 只是协调观测。members 标注消费能力和并行分区数。

## 浏览与检查

在仓库根目录使用 Python 3.11 标准库。

```sh
python3 read_sources.py examples/shift.jsonl
python3 read_sources.py examples/contrast.jsonl
python3 -m unittest discover -s tests -v
```

读取工具按原顺序显示观察。结尾的来源完整性检查只涉及清册和记录。`--kind` 可筛选类型。
