# README for POX Firewall

Welcome to the POX Firewall project! This README provides a step-by-step guide on how to set up and run the POX Firewall controller using OpenFlow.

## Getting Started

To begin, follow these instructions to clone the repository and set up the necessary components.

### Prerequisites

Before you proceed, ensure that you have the following installed on your system:

- Python 3.x
- git
- mininet

### Installation

1. Clone the repository:

git clone https://github.com/noxrepo/pox.git

2. Move the required files to the POX directory:

mv firewall_rules_config.json pox
mv topology.py pox
mv firewall.py pox/pox/misc/

3. Change to the POX directory:

cd pox

## Running the Firewall

To run the POX Firewall controller and a sample topology, follow the instructions below:

### Step 1: Run POX controller

Open a terminal and run the POX controller with the following command:

./pox.py log.level --DEBUG openflow.of_01 forwarding.l2_learning misc.firewall

### Step 2: Start the sample topology

In a second terminal, initiate the sample topology using the provided Python script:

sudo python3 topology.py

Please note that `sudo` is required to set up network configurations.

## Configuration

The `firewall_rules_config.json` file contains the rules for the firewall. Make sure to configure the rules according to your requirements before running the controller.

