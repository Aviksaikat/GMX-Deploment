#!/usr/bin/python3
import json
import os
from collections import defaultdict
from datetime import datetime

# Define the deployments directory
DEPLOYMENTS_DIR = "gmx-synthetics/deployments"

# Define mainnet and testnet identifiers
MAINNETS = {"arbitrum", "avalanche"}
TESTNETS = {"arbitrumGoerli", "arbitrumSepolia", "avalancheFuji"}

# Initialize data structures
network_data = defaultdict(lambda: defaultdict(list))

# Traverse the deployments directory
for network in os.listdir(DEPLOYMENTS_DIR):
    network_path = os.path.join(DEPLOYMENTS_DIR, network)
    if os.path.isdir(network_path):
        # Determine if the network is mainnet or testnet
        if network in MAINNETS:
            net_type = "Mainnet"
        elif network in TESTNETS:
            net_type = "Testnet"
        else:
            net_type = "Other"

        # Process JSON files in the network directory
        for file in os.listdir(network_path):
            if file.endswith(".json"):
                file_path = os.path.join(network_path, file)
                try:
                    with open(file_path, "r") as f:
                        data = json.load(f)
                        address = data.get("address")
                        if address:
                            contract_name = os.path.splitext(file)[0]
                            network_data[net_type][network].append(
                                (contract_name, address)
                            )
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

# Get current date
current_date = datetime.utcnow().strftime("%d %b %Y")

# Write to README.md
with open("README.md", "w") as md_file:
    md_file.write(f"# 📄 GMX Deployed Contracts as of {current_date}\n\n")
    for net_type in ["Mainnet", "Testnet", "Other"]:
        if network_data[net_type]:
            md_file.write(f"## 🌐 {net_type}\n\n")
            for network in sorted(network_data[net_type]):
                md_file.write(f"### 🧭 {network}\n\n")
                md_file.write("| Contract Name | Address |\n")
                md_file.write("|---------------|---------|\n")
                for contract_name, address in sorted(network_data[net_type][network]):
                    md_file.write(f"| {contract_name} | `{address}` |\n")
                md_file.write("\n")
    md_file.write(f"---\n\n_Last updated: {current_date}_\n")
