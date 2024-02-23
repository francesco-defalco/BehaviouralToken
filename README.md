# Behavioural Token Smart Contract

## Introduction
The Behavioural Token is an ERC-20 compliant token designed to incentivize and reward customers for virtuous behaviours as identified by service providers. This innovative blockchain solution is applicable across various sectors, including but not limited to insurance companies and energy suppliers. It aims to establish an ecosystem where businesses can reward customers for positive actions, such as safe driving or low energy consumption.

## Key Entities
The system incorporates three primary entities:
1. **Owner**: Contract owner with overarching control privileges.
2. **Service Provider**: Entities that can add customers and distribute tokens as rewards.
3. **Customer**: Individuals who receive tokens for virtuous behaviours and can spend them within the ecosystem.

## Features
- **ERC-20 Compliance**: Adheres to the ERC-20 token standard for Ethereum, ensuring compatibility with a broad range of services and wallets.
- **Role-Based Access Control (RBAC)**: Implements access control based on roles to differentiate the capabilities of Owners, Service Providers, and Customers within the system.
- **Pausable**: The contract can be paused by the Owner to temporarily halt all activities in case of emergencies.
- **Nonce for Meta-Transactions**: Supports meta-transactions, allowing customers to interact with the contract without directly spending gas.
- **Token-to-Ether Rate**: Establishes an exchange rate between Ether and Behavioural Tokens, enabling Service Providers to purchase tokens.

## Core Functionalities
- **Role Management**: Functions to add or remove Service Providers and Customers from the ecosystem.
- **Token Purchase**: Service Providers can buy tokens by sending Ether to the contract.
- **Rewards and Purchases**: Customers can spend their tokens to purchase services or receive discounts.
- **Secure Transactions**: Uses ECDSA cryptography to verify the authenticity of meta-transactions.
- **Supply Management**: The Owner can increase the total supply of tokens in circulation.

## Contract Deployment
Compile and deploy the contract to the desired environment following the specific documentation of the used framework (e.g., Truffle, Hardhat).

## Initial Configuration
After deployment, the contract owner can set up Service Providers and the Ether-to-token exchange rate using the exposed contract functions.

## Security
The contract incorporates various security measures, including pause controls and role management. A comprehensive code audit is recommended before production use to identify and mitigate potential vulnerabilities.

## License
The source code for the Behavioural Token is released under the MIT license.

## Contribution
Contributions are welcome! For bug reports or feature requests, please open an issue through GitHub. Ensure your contributions adhere to the project's coding standards and guidelines.

