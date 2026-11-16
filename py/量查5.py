# 量查5（第 21 天 20:4x，吹万 20:29 段）：接查二1 那一下"询问也在制造新版本"。
# 你去问一户"听说你说我……？"，等于把村口那句（最坏那句）又递给它一回：它照脾气改了，再传给邻居，新的盖掉旧的。
# 问是要读脾气，可问到"怕"的那户，它把最坏那句又往坏里传一圈。问谁 = 读得多 和 传得坏 之间挑。
# 量：两问，每一对问法各算 猜对（同量查4，偏宽、知道树）和 问完以后全村平均坏（每问一次传一整圈）。
import itertools, sys
from 查2 import 开局, 名, 脾气们, 讲给你, 邻
from 村 import 念, 坏

def 链(听过, 末人):
    路 = []; 人 = 末人
    while 人 != "你": 路.append(人); 人 = 听过[人][1]
    return 路[::-1]
def 跑(村, 起, s, 树):
    听过 = {}
    for 人 in 树["序"]:
        从 = 树["从"][人]; 句 = dict(s if 从 == "你" else 听过[从][0]); 改 = 村[人](句)
        听过[人] = (句, 从, 改)
    return 听过
def 打分(句, s): return 句["动"] * 2 + 句["久"] + (句["在"] != s["在"]) * 2

def 回传(村, 现, 谁, 句):  # 把句递给"谁"，它改了传一整圈（每户这一圈只传一次），新的盖旧的
    现 = dict(现); 队 = [(谁, dict(句))]; 过 = set()
    while 队:
        人, 句 = 队.pop(0)
        if 人 in 过: continue
        过.add(人); 句 = dict(句); 村[人](句); 现[人] = 句
        for x in 邻[人]: 队.append((x, 句))
    return 现

N = int(sys.argv[1]) if len(sys.argv) > 1 and __name__ == "__main__" else (200 if __name__ == "__main__" else 0)
全 = [dict(zip(名, p)) for p in itertools.permutations(脾气们)]
合 = {"乱": [0, 0], "读最好": [0, 0], "坏最少": [0, 0], "起头+乱": [0, 0], "不问": [0, 0]}
同 = 0; 差 = []
for seed in range(N):
    村, 起, s, 听过 = 开局(seed)
    树 = {"序": list(听过), "从": {k: v[1] for k, v in 听过.items()}}
    def 末与凶(h):
        末 = max(h.items(), key=lambda kv: 打分(kv[1][0], s))
        for 人 in 链(h, 末[0]):
            if h[人][2] != "原样" and h[人][0] != (s if h[人][1] == "你" else h[h[人][1]][0]): return 末, 人
        return 末, None
    末, 真凶 = 末与凶(听过); 真末 = 念(末[1][0]); 末句 = 末[1][0]
    各 = []
    for 村2 in 全:
        h = 跑(村2, 起, s, 树); m, c = 末与凶(h)
        if 念(m[1][0]) == 真末: 各.append((村2, h, c))
    def 猜对(问):
        剩 = [c for 村2, h, c in 各 if all(念(讲给你(村2, q, h[q][0])) == 念(讲给你(村, q, 听过[q][0])) for q in 问 if q in 听过)]
        if not 剩: return 0
        return sum(1 for c in 剩 if c == 真凶) / len(剩)
    原 = {k: v[0] for k, v in 听过.items()}
    def 坏了(问):
        现 = 原
        for q in 问: 现 = 回传(村, 现, q, 末句)
        return sum(坏(x) for x in 现.values()) / len(现)
    人们 = [n for n in 名 if n in 听过]
    对 = [(q, 猜对(q), 坏了(q)) for q in itertools.combinations(人们, 2)]
    合["不问"][0] += 猜对([]); 合["不问"][1] += sum(坏(x) for x in 原.values()) / len(原)
    合["乱"][0] += sum(a for _, a, _ in 对) / len(对); 合["乱"][1] += sum(b for _, _, b in 对) / len(对)
    好 = max(对, key=lambda t: (t[1], -t[2])); 少 = min(对, key=lambda t: (t[2], -t[1]))
    合["读最好"][0] += 好[1]; 合["读最好"][1] += 好[2]
    合["坏最少"][0] += 少[1]; 合["坏最少"][1] += 少[2]
    带 = [t for t in 对 if 起 in t[0]]
    合["起头+乱"][0] += sum(a for _, a, _ in 带) / len(带); 合["起头+乱"][1] += sum(b for _, _, b in 带) / len(带)
    同 += (好[0] == 少[0])
    # 每一对里：猜对 ≥0.9 的问法中，坏最少的 比 读最好那对 少多少坏
    够 = [t for t in 对 if t[1] >= 0.9]
    if 够: 差.append(好[2] - min(t[2] for t in 够))
for k, (a, b) in (合.items() if N else []): print(f"{k:6} 猜对 {a / N:.2f}　问完全村平均坏 {b / N:.2f}")
if N: print(f"读最好那对 = 坏最少那对 的局：{同}/{N}")
if 差: print(f"猜对≥0.9 里挑坏最少的，比读最好那对平均少坏 {sum(差) / len(差):.2f}（{len(差)} 局有这种问法）")
