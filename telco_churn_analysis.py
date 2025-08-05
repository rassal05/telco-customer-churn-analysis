import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("PROJECT1.csv")

#TotalCharges column cleaning

df["TotalCharges"] = df["TotalCharges"].replace(" ", np.nan)
df["TotalCharges"] = df["TotalCharges"].astype(float)
df["TotalCharges"].fillna(df["TotalCharges"].mean(), inplace=True)

#Converting churn to numerical value

df["Churn"].replace({"Yes": 1, "No": 0}, inplace=True)

#Summary Text

total_customers = df.shape[0]
churned = df["Churn"].sum()
stayed = total_customers - churned
churn_rate = churned / total_customers * 100
avg_monthly_charges_churn = df[df["Churn"] == 1]["MonthlyCharges"].mean()
avg_monthly_charges_stay = df[df["Churn"] == 0]["MonthlyCharges"].mean()

#Set dashboard layout

plt.figure(figsize=(36, 24))
sns.set_style("whitegrid")
sns.set_palette("viridis")

#Summary

plt.subplot(3, 3, 1)
plt.axis('off')

summary_text = f"""
 Total Customers: {total_customers}
 Churned Customers: {churned}
 Stayed Customers: {stayed}
 Churn Rate: {churn_rate:.2f}%
 Avg Monthly Charge (Churned): ${avg_monthly_charges_churn:.2f}
 Avg Monthly Charge (Stayed): ${avg_monthly_charges_stay:.2f}
"""
plt.text(0.1, 0.8, "Customer Churn Summary", fontsize=37, weight='bold', fontfamily="monospace", va='top')
plt.text(0.1, 0.7, summary_text, fontsize=33, fontfamily="monospace", va='top')

 
#Churn by Tenure

tenure_churn = df.groupby("tenure")["Churn"].mean().reset_index()
tenure_churn["Churn"] *= 100
plt.subplot(3, 3, 2)
sns.lineplot(data=tenure_churn, x="tenure", y="Churn", marker="o", color="orange",weights="Churn")
plt.title("Churn Rate by Tenure",weight="bold",fontsize=33)
plt.xlabel("Tenure (months)",fontsize=29)
plt.ylabel("Churn Rate (%)",fontsize=29)
plt.xticks(fontsize=27)
plt.yticks(fontsize=27)

#Churn by Senior Citizen

df["SeniorCitizen"].replace({0: "Youngsters", 1: "Senior Citizens"}, inplace=True)
senior_churn = df.groupby("SeniorCitizen")["Churn"].mean().reset_index()
senior_churn["Churn"] *= 100
plt.subplot(3, 3, 3)
sns.barplot(data=senior_churn, x="SeniorCitizen", y="Churn",palette="viridis")
plt.title("Churn by Senior Citizen Type",weight="bold",fontsize=33)
plt.xlabel("Citizen Type",fontsize=29)
plt.ylabel("Churn Rate (%)",fontsize=29)
plt.xticks(fontsize=27)
plt.yticks(fontsize=27)

#Churn by Contract

contract_churn = df.groupby("Contract")["Churn"].mean().reset_index()
contract_churn["Churn"] *= 100
explode = [0.05, 0, 0]
plt.subplot(3, 3, 4)
plt.pie(contract_churn["Churn"], labels=contract_churn["Contract"], autopct="%.1f%%",pctdistance=1.3,labeldistance=1.5, explode=explode,textprops={'fontsize':25,'color':'black'})
plt.title("Churn by Contract Type",weight="bold",fontsize=29)

#Churn by Payment Method

payment_churn = df.groupby("PaymentMethod")["Churn"].mean().reset_index()
payment_churn["Churn"] *= 100
payment_churn["PaymentMethod"] = payment_churn["PaymentMethod"].replace({
    "Bank transfer (automatic)": "Bank Transfer",
    "Credit card (automatic)": "Credit Card"
})
plt.subplot(3, 3, 5)
sns.barplot(data=payment_churn, x="PaymentMethod", y="Churn",palette="viridis")
plt.title("Churn by Payment Method",weight="bold",fontsize=33)
plt.xlabel("Payment Method",fontsize=29)
plt.ylabel("Churn(%)",fontsize=29)
plt.xticks(rotation=15,fontsize=27)
plt.yticks(fontsize=27)

#Churn by Internet Service

internet_churn = df.groupby("InternetService")["Churn"].mean().reset_index()
internet_churn["Churn"] *= 100
plt.subplot(3, 3, 6)
sns.barplot(data=internet_churn, x="InternetService", y="Churn",palette="viridis")
plt.xlabel("Internet Service",fontsize=29)
plt.ylabel("Churn(%)",fontsize=29)
plt.title("Churn by Internet Service",weight="bold",fontsize=33)
plt.xticks(fontsize=27)
plt.yticks(fontsize=27)

#Churn by Device Protection

df_filtered = df[df["DeviceProtection"] != "No internet service"]
device_churn = df_filtered.groupby("DeviceProtection")["Churn"].mean().reset_index()
device_churn["Churn"] *= 100
plt.subplot(3, 3, 7)
sns.barplot(data=device_churn, x="DeviceProtection", y="Churn",palette="viridis")
plt.title("Churn by Device Protection",weight="bold",fontsize=33)
plt.xlabel("Device Protection",fontsize=29)
plt.ylabel("Churn(%)",fontsize=29)
plt.xticks(rotation=15,fontsize=27)
plt.yticks(fontsize=27)

#Average Charges Comparison

avg_data = {
    'Churn': ['Stayed', 'Churned'],
    'MonthlyCharges': [avg_monthly_charges_stay, avg_monthly_charges_churn],
    'TotalCharges': [
        df[df["Churn"] == 0]["TotalCharges"].mean(),
        df[df["Churn"] == 1]["TotalCharges"].mean()
    ]
}
avg_df = pd.DataFrame(avg_data)

#Monthly Charges Plot

plt.subplot(3, 3, 8)
sns.barplot(data=avg_df, x="Churn", y="MonthlyCharges",palette="viridis")
plt.title("Avg Monthly Charges",weight="bold",fontsize=33)
plt.xlabel("Churn",fontsize=29)
plt.ylabel("Monthly Charges",fontsize=29)
for i, v in enumerate(avg_df["MonthlyCharges"]):
    plt.text(i, v + 1, f'{v:.2f}', ha='center')
plt.xticks(fontsize=27)
plt.yticks(fontsize=27)

#Total Charges Plot

plt.subplot(3, 3, 9)
sns.barplot(data=avg_df, x="Churn", y="TotalCharges",palette="viridis")
plt.title("Avg Total Charges",weight="bold",fontsize=33)
plt.xlabel("Churn",fontsize=29)
plt.ylabel("Total Charges",fontsize=29)
for i, v in enumerate(avg_df["TotalCharges"]):
    plt.text(i, v + 20, f'{v:.2f}', ha='center')
plt.xticks(fontsize=27)
plt.yticks(fontsize=27)

#Displaying Dashboard

plt.suptitle("TELCO CUSTOMER CHURN DASHBOARD", fontsize=45 , weight="bold")
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.gcf().set_facecolor("#e0f7fa")
plt.savefig("telco_churn_dashboard.png", dpi=300, facecolor="#e0f7fa")
plt.show()
