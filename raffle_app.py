import streamlit as st
import pandas as pd
import yagmail

# 景品リスト
prizes = ["Prize A", "Prize B", "Prize C", "Prize D"]

# 投票結果を格納するデータフレーム
if "votes" not in st.session_state:
    st.session_state.votes = {prize: 0 for prize in prizes}

# ヘッダー
st.title("Virtual Raffle Voting System 🎟️")
st.write("Distribute your tickets to the prizes you like!")

# 参加者の名前とチケット枚数を入力
name = st.text_input("Enter your name:", key="name")
tickets = st.number_input("Enter the number of tickets you have:", min_value=1, step=1, key="tickets")

# 投票セクション
if name and tickets:
    st.write("Distribute your tickets among the prizes:")
    ticket_distribution = {}
    remaining_tickets = tickets

    for prize in prizes:
        num_tickets = st.number_input(
            f"How many tickets do you want to assign to {prize}?",
            min_value=0,
            max_value=remaining_tickets,
            step=1,
            key=f"{name}_{prize}",
        )
        ticket_distribution[prize] = num_tickets
        remaining_tickets -= num_tickets

    # 投票を記録
    if remaining_tickets == 0:
        if st.button("Submit Your Votes"):
            for prize, num_tickets in ticket_distribution.items():
                st.session_state.votes[prize] += num_tickets
            st.success("Thank you for voting!")
            st.write("Here is your ticket distribution:")
            st.write(ticket_distribution)
    elif remaining_tickets > 0:
        st.warning(f"You have {remaining_tickets} tickets remaining. Please allocate them all.")

# 結果表示セクション
st.write("### Current Voting Results:")
results_df = pd.DataFrame(
    {"Prize": list(st.session_state.votes.keys()), "Votes": list(st.session_state.votes.values())}
)
st.table(results_df)

# メール送信
admin_email = st.text_input("Enter admin email to send results:")
if st.button("Send Results to Admin"):
    try:
        yag = yagmail.SMTP("your_email@example.com", "your_password")  # 自分のメールアドレスとパスワード
        yag.send(
            to=admin_email,
            subject="Raffle Voting Results",
            contents=results_df.to_csv(index=False),
        )
        st.success(f"Results sent to {admin_email} successfully!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")
