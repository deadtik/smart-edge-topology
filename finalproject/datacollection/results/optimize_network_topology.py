import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Step 1: Load Network Metrics CSV with tab delimiter
try:
    df = pd.read_csv("network_metrics.csv", delimiter='\t')
    df.columns = df.columns.str.strip()  # Remove any whitespace from column names
    print("Headers detected in the CSV:", df.columns.tolist())
except Exception as e:
    print("Error reading the CSV:", e)
    exit()

# Step 2: Check required columns
required_columns = ['Topology_Type', 'Latency_ms', 'Bandwidth_Mbps', 'Jitter_ms', 'Packet_Loss_%']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print("Missing columns:", missing_columns)
    exit()

# Step 3: Normalize the metrics (inverting latency & packet loss for better ranking)
scaler = MinMaxScaler()

df['norm_latency'] = 1 - scaler.fit_transform(df[['Latency_ms']])  # Lower latency is better
df['norm_bandwidth'] = scaler.fit_transform(df[['Bandwidth_Mbps']])  # Higher is better
df['norm_jitter'] = 1 - scaler.fit_transform(df[['Jitter_ms']])  # Lower jitter is better
df['norm_packet_loss'] = 1 - scaler.fit_transform(df[['Packet_Loss_%']])  # Lower is better

# Step 4: Define Weights (Higher impact to latency & bandwidth)
weights = {
    'norm_latency': 0.5,  # Latency has the highest importance
    'norm_bandwidth': 0.3,  # Bandwidth contributes significantly
    'norm_jitter': 0.1,  # Jitter is less important
    'norm_packet_loss': 0.1  # Packet loss is also considered
}

# Step 5: Calculate QoS Score (Weighted Sum)
df['score'] = (
    df['norm_latency'] * weights['norm_latency'] +
    df['norm_bandwidth'] * weights['norm_bandwidth'] +
    df['norm_jitter'] * weights['norm_jitter'] +
    df['norm_packet_loss'] * weights['norm_packet_loss']
)

# Step 6: Identify Best Topology Before Optimization (Minimum Latency & Best QoS)
best_before = df.nsmallest(1, 'Latency_ms')  # Find topology with the lowest latency

# Step 7: Identify Best Topology After Optimization (Highest QoS Score)
best_after = df.nlargest(1, 'score')

# Step 8: Display Results
print("\nBest Topology Before Optimization:")
print(best_before[['Topology_Type', 'Latency_ms', 'Bandwidth_Mbps', 'Jitter_ms', 'Packet_Loss_%']])

print("\nBest Topology After Optimization:")
print(best_after[['Topology_Type', 'score', 'Latency_ms', 'Bandwidth_Mbps', 'Jitter_ms', 'Packet_Loss_%']])

# Step 9: Comparison Table
comparison_df = pd.DataFrame({
    'Metric': ['Latency (ms)', 'Bandwidth (Mbps)', 'Jitter (ms)', 'Packet Loss (%)'],
    'Before': best_before[['Latency_ms', 'Bandwidth_Mbps', 'Jitter_ms', 'Packet_Loss_%']].values[0],
    'After': best_after[['Latency_ms', 'Bandwidth_Mbps', 'Jitter_ms', 'Packet_Loss_%']].values[0]
})

print("\nComparison (Before vs. After):")
print(comparison_df)

# Step 10: Visualization of Topologies (Latency, Bandwidth, QoS)
fig, ax = plt.subplots(1, 3, figsize=(18, 6))

# Latency vs Bandwidth
ax[0].scatter(df['Latency_ms'], df['Bandwidth_Mbps'], c='blue', label='Topologies')
ax[0].scatter(best_before['Latency_ms'], best_before['Bandwidth_Mbps'], color='green', label='Best Before')
ax[0].scatter(best_after['Latency_ms'], best_after['Bandwidth_Mbps'], color='red', label='Best After')
ax[0].set_xlabel('Latency (ms)')
ax[0].set_ylabel('Bandwidth (Mbps)')
ax[0].set_title('Latency vs Bandwidth')
ax[0].legend()

# Jitter vs Packet Loss
ax[1].scatter(df['Jitter_ms'], df['Packet_Loss_%'], c='blue', label='Topologies')
ax[1].scatter(best_before['Jitter_ms'], best_before['Packet_Loss_%'], color='green', label='Best Before')
ax[1].scatter(best_after['Jitter_ms'], best_after['Packet_Loss_%'], color='red', label='Best After')
ax[1].set_xlabel('Jitter (ms)')
ax[1].set_ylabel('Packet Loss (%)')
ax[1].set_title('Jitter vs Packet Loss')
ax[1].legend()

# QoS Score vs Topology Type
ax[2].bar(df['Topology_Type'], df['score'], color='blue', label='QoS Score')
ax[2].bar(best_before['Topology_Type'], best_before['score'], color='green', label='Best Before')
ax[2].bar(best_after['Topology_Type'], best_after['score'], color='red', label='Best After')
ax[2].set_xlabel('Topology Type')
ax[2].set_ylabel('QoS Score')
ax[2].set_title('QoS Score by Topology')
ax[2].legend()

plt.tight_layout()
plt.show()
