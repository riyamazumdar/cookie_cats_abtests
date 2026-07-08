import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="090627",
    database="cookie_cats_ab"
)
df = pd.read_sql("SELECT * FROM player_data", conn)
conn.close()

print(df.shape)
print(df.head())

df["retention_1"]=df["retention_1"].astype(int)
df["retention_7"]=df["retention_7"].astype(int)

gate_30 = df[df["version"]== "gate_30"]
gate_40 = df[df["version"]== "gate_40"]

print(f"gate_30: {len(gate_30)} players")
print(f"gate_40: {len(gate_40)} players")

#checks whether the retention differnece we saw was real or just noise
import numpy as np
from scipy import stats

def two_proportion_z_test(sucess_a, n_a, sucess_b, n_b):
    p_a = sucess_a/n_a
    p_b = sucess_b/n_b
    p_pool= (sucess_a+sucess_b)/(n_a+n_b)
    se = np.sqrt(p_pool*(1-p_pool)*(1/n_a+1/n_b))
    z= (p_a-p_b)/se
    p_value=2*(1-stats.norm.cdf(abs(z)))
    return p_a,p_b,z,p_value
success_30_r1=gate_30["retention_1"].sum()
success_40_r1=gate_40["retention_1"].sum()
n_30=len(gate_30)
n_40=len(gate_40)

p_30_r1, p_40_r1, z_r1, p_val_r1= two_proportion_z_test(success_30_r1, n_30, success_40_r1, n_40)
print(f"\nretention_1 - gate_30:{p_30_r1*100:.2f}%, gate_40:{p_40_r1*100:.2f}%")
print(f"z-statistic: {z_r1:.3f}, p-value: {p_val_r1:.4f}")

success_30_r7=gate_30["retention_7"].sum()
success_40_r7=gate_40["retention_7"].sum()
n_30=len(gate_30)
n_40=len(gate_40)

p_30_r7, p_40_r7, z_r7, p_val_r7= two_proportion_z_test(success_30_r7, n_30, success_40_r7, n_40)
print(f"\nretention_7 - gate_30:{p_30_r7*100:.2f}%, gate_40:{p_40_r7*100:.2f}%")
print(f"z-statistic: {z_r7:.3f}, p-value: {p_val_r7:.4f}")
