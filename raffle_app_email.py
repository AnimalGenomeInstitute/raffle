import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# 環境変数からGmailアカウント情報を取得
GMAIL_USER = os.getenv("")
GMAIL_PASSWORD = os.getenv("")

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

            # 投票結果をGmailで送信
            recipient_email = st.text_input("Enter your email to receive results:", key="email")
            if recipient_email:
                if st.button("Send Results to Gmail"):
                    try:
                        # メールを作成
                        message = MIMEMultipart()
                        message["From"] = GMAIL_USER
                        message["To"] = recipient_email
                        message["Subject"] = "Your Voting Results"

                        # メール本文
                        body = (
                            f"Hello {name},\n\n"
                            f"Thank you for participating in the raffle voting!\n\n"
                            f"Here is your ticket distribution:\n"
                        )
                        for prize, num_tickets in ticket_distribution.items():
                            body += f"- {prize}: {num_tickets} tickets\n"

                        message.attach(MIMEText(body, "plain"))

                        # Gmailサーバーに接続して送信
                        with smtplib.SMTP("smtp.gmail.com", 587) as server:
                            server.starttls()
                            server.login(GMAIL_USER, GMAIL_PASSWORD)
                            server.send_message(message)

                        st.success("Results have been sent to your email!")
                    except Exception as e:
                        st.error(f"An error occurred while sending the email: {e}")
    elif remaining_tickets > 0:
        st.warning(f"You have {remaining_tickets} tickets remaining. Please allocate them all.")

# 結果表示セクション
st.write("### Current Voting Results:")
results_df = pd.DataFrame(
    {"Prize": list(st.session_state.votes.keys()), "Votes": list(st.session_state.votes.values())}
)
st.table(results_df)
