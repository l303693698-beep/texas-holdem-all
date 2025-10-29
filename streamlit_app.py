import streamlit as st
from treys import Card, Evaluator, Deck

st.set_page_config(page_title="德州扑克胜率计算器", page_icon="♠️", layout="centered")

st.title("♠️ 德州扑克胜率计算器")

st.markdown("""
输入你的两张手牌（Hero）和对手的两张手牌（Villain），
点击“开始计算”即可查看大致胜率（蒙特卡洛模拟）。
示例输入格式：
- Hero: `As Ah`
- Villain: `2d 7c`
""")

hero_input = st.text_input("Hero 手牌", "As Ah")
villain_input = st.text_input("Villain 手牌", "2d 7c")
iterations = st.slider("模拟次数（越多越精确，但速度稍慢）", 1000, 200000, 50000, step=10000)

def simulate(hero, villain, iterations):
    evaluator = Evaluator()
    hero_wins = ties = 0
    for _ in range(iterations):
        deck = Deck()
        hero_cards = [Card.new(c) for c in hero]
        villain_cards = [Card.new(c) for c in villain]
        for c in hero_cards + villain_cards:
            deck.cards.remove(c)
        board = deck.draw(5)
        hero_score = evaluator.evaluate(board, hero_cards)
        villain_score = evaluator.evaluate(board, villain_cards)
        if hero_score < villain_score:
            hero_wins += 1
        elif hero_score == villain_score:
            ties += 1
    return (hero_wins + ties/2) / iterations

if st.button("开始计算"):
    try:
        hero = hero_input.split()
        villain = villain_input.split()
        eq = simulate(hero, villain, iterations)
        st.success(f"Hero 胜率约为 **{eq*100:.2f}%** 🎯")
    except Exception as e:
        st.error(f"输入有误：{e}")
