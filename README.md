# CalmBot: Your Companion for Inner Peace 🌱

**CalmBot** is an AI-powered emotional support platform designed to help users heal from unresolved trauma and find peace amidst life’s chaos. Built for the **Peace with Oneself** problem statement at Hackathon 2025, CalmBot empowers individuals to recognize, monitor, and mend deep-rooted emotional wounds, often stemming from childhood hurts or societal neglect.

We are looking to develop the first AI companion that deals with inner peace using users' mobile devices, incentivizing them when they use the app through blockchain-based rewards. Whether you’re feeling happy, sad, angry, or anxious, CalmBot offers empathetic guidance, personalized actions, and a safe space to reflect—fostering resilience and self-compassion.

Accessible via a responsive website, a Telegram bot, and future mobile apps, CalmBot ensures users can seek support anytime, anywhere. Powered by Google’s Gemini model and a custom learning model with adaptive memory, CalmBot delivers trauma-aware responses and grows smarter by learning from user interactions.

To make CalmBot decentralized, we've integrated blockchain features built on the U2U Network, a scalable Layer-1 blockchain platform. This allows for secure, transparent data storage, user-owned emotional journals, and token-based incentives for engagement. Users can earn U2U-compatible tokens (or a custom CalmToken) for completing journaling sessions, breathing exercises, or mindfulness activities, which can be redeemed for premium features, community rewards, or even staked for governance in the CalmBot ecosystem. This web3 integration promotes a user-to-user (U2U) network where individuals support each other's healing journeys in a decentralized manner.

Everything is in order, and we are just looking for funding to deploy it to the testnet and then mainnet on the U2U Network. This will be great!

## 🧠 Problem Statement: Peace with Oneself

The **Peace with Oneself** challenge calls for solutions to help individuals heal from emotional distress and unresolved trauma, which often originate in childhood and are exacerbated by external chaos. CalmBot addresses this by:

- **Acknowledging Trauma:** Recognizes potential wounds (e.g., neglect, betrayal) with empathy, validating users’ emotions.
- **Empowering Healing:** Offers actionable steps like journaling, breathing exercises, and mindfulness to process pain, with blockchain rewards to incentivize consistent use.
- **Building Resilience:** Motivates users to break cycles of avoidance and find strength in their journey, earning tokens for progress milestones.
- **Creating Calm:** Provides tools like the Serenity Garden and chat support to anchor users in peace, all secured on the decentralized U2U blockchain.

CalmBot is more than a tool—it’s a companion for those seeking to reclaim their emotional well-being and thrive, now enhanced with web3 decentralization for true user empowerment.

---

## 🌟 Features

- **Emotion-Based Support:** Choose from *Happy*, *Sad*, *Angry*, or *Anxious* to receive tailored, empathetic responses that address trauma and suggest healing actions.
- **Serenity Garden:** A virtual space to plant flowers with soothing bird and forest sounds to promote mindfulness and calm.
- **Journaling:** Reflect on emotions with guided prompts, storing entries securely on the blockchain to ensure user ownership and privacy.
- **Breathing Exercises:** Guided 4-4-8 breathing to reduce stress and ground users in the present.
- **Your Emotional Journey:** Visualize mood trends with a bar chart, celebrating progress in emotional awareness.
- **Chat Mode:** Engage in freeform conversations via the website or Telegram bot, with responses that adapt to your emotional state.
- **Blockchain Incentives:** Earn tokens on the U2U Network for daily app usage, completing healing activities, or sharing anonymized insights to build a community-driven knowledge base.

### Dual AI Models
- **Gemini Model:** Powers empathetic, trauma-aware responses for real-time support.
- **Custom Learning Model:** Learns from unknown inputs by asking for clarification, storing new knowledge for future interactions, with decentralized storage on U2U.

### Multi-Platform Access
- **Website:** Beautiful, responsive design for immersive support, with wallet integration for web3 features.
- **Telegram Bot:** Instant access via social platforms, perfect for on-the-go users, including mobile token claims.

### Mental Health Resources
- Links to trusted services like BetterHelp and Crisis Text Line for additional support.

---

## 🛠 Tech Stack

### Backend
- **Python**
- **Flask**
- **SQLite** (for local caching, with blockchain for persistent data)
- **Google Generative AI (Gemini)**
- **TextBlob**
- **python-telegram-bot**

### Frontend
- **HTML5/CSS3**
- **JavaScript**
- **Tailwind CSS**
- **Google Fonts (Poppins)**
- **p5.js**

### Web3 Integration
- **U2U Network SDK** (for blockchain interactions and DePIN features)
- **Solidity** (for smart contracts, assuming EVM compatibility or equivalent on U2U)
- **Web3.py** (Python library for backend blockchain integration)
- **Web3.js** (JavaScript library for frontend wallet connections and token management)
- **IPFS** (for decentralized storage of user journals and media)
- **WalletConnect** (for seamless mobile wallet integration)

### Tools & APIs
- **Gemini API**
- **Telegram API**
- **python-dotenv**
- **Freesound.org** (bird and forest sounds)
- **U2U Network API** (for token minting, staking, and governance)

### Infrastructure
- **GitHub**
- **Local Windows Dev**
- **SQLite Database** (hybrid with U2U blockchain for decentralization)
- **U2U Testnet/Mainnet** (for deployment of smart contracts and dApp features)

---

## 🔍 How It Works

### Access CalmBot
- Website: https://bot-1-txcf.onrender.com/
- Telegram: Search for `@calm56bot`

### Select Your Mood
Click *Happy*, *Sad*, *Angry*, or *Anxious* to receive a Gemini-powered response, and earn micro-rewards for engagement.

### Engage with Features
- **Serenity Garden:** Plant flowers and enjoy ambient sounds, minting NFTs of your garden on U2U for personal ownership.
- **Journal:** Reflect on guided prompts, with entries tokenized for secure, decentralized access.
- **Breathing:** Try calming breathing exercises, tracked on-chain for reward eligibility.
- **Chat:** Use `/chat` on Telegram or the website chatbox, with adaptive responses and incentive tracking.

### Adaptive Learning
- CalmBot asks for clarification when it encounters unknown inputs.
- Stores user-defined meanings in memory (`unknown_inputs.json`) and on the U2U blockchain for decentralized knowledge sharing.

### Track Progress
- Mood history and emotional trends are visualized and securely stored in `mood_tracker.db`, synced to the blockchain for immutability.

### Web3 Incentives
- Connect your wallet to claim tokens earned from app usage.
- Stake tokens to vote on new features or community healing initiatives.

---

## 💻 Installation

```bash
git clone https://github.com/barnazaka/bot.git
cd bot
pip install flask python-telegram-bot google-generativeai python-dotenv textblob web3
python -m textblob.download_corpora
```

### Set Up Environment

Create a `.env` file in the `calmbot/` directory:

```
TELEGRAM_TOKEN=your_telegram_token
GOOGLE_API_KEY=your_gemini_api_key
U2U_RPC_URL=your_u2u_rpc_url
WALLET_PRIVATE_KEY=your_wallet_private_key  # For development only
```

* Place `index.html` in `calmbot/templates/`
* Place audio files in `calmbot/static/`

### Run the Website

```bash
python server.py
```

Access at `http://localhost:5000`

### Run the Telegram Bot

```bash
python calmbot.py
```

### Deploy Smart Contracts
Use Truffle or Hardhat for Solidity contracts on U2U testnet.

---

## 🚀 Usage

### Website

* Select a mood, explore the Serenity Garden, start journaling, or chat.
* Track your healing journey visually and claim web3 rewards.

### Telegram Bot

* Use `/start` to begin.
* Select a mood or type `/chat` to talk freely.
* Use `/claim` to redeem earned tokens.
* Responses are adaptive and emotionally aware.

### Example Interaction

```text
User: I'm feeling stressed.
CalmBot: Stress can feel so heavy, often tied to life’s chaos or past worries. Try a 4-4-8 breathing exercise: inhale for 4, hold for 4, exhale for 8. Want to share more? I’m here. You've earned 10 CalmTokens for this session!

User: xyz
CalmBot: I don’t know what you mean by "xyz," but I’ll learn! Can you explain it? Let’s keep chatting.
```

---

## 💖 Why CalmBot?

* **Trauma-Aware Design:** Tackles childhood wounds and emotional pain with empathy.
* **Dual AI Approach:** Combines Gemini’s power with a custom learner for personalization.
* **Accessible Platforms:** Website and Telegram support available 24/7, with mobile incentives.
* **Holistic Healing:** Journaling, breathing, mindfulness, and conversation in one place, incentivized via blockchain.
* **Privacy-First:** Stores data locally with SQLite and on U2U blockchain for user security, ownership, and trust.
* **Decentralized Web3:** Empowers users with token rewards and governance on the U2U Network.

---

## 📈 Future Enhancements

* Mobile App (iOS/Android) with full web3 wallet integration
* Deeper Learning Personalization using on-chain data
* Multilingual Support
* Wearable Device Integration
* Community Sharing & Support via decentralized forums
* Full deployment to U2U mainnet after funding

---

## 🤝 Contributing

We welcome contributions!

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`.
3. Commit changes: `git commit -m "Add your feature"`.
4. Push: `git push origin feature/your-feature`.
5. Open a pull request.

Please review our **Code of Conduct** and use **GitHub Issues** for feedback or bugs.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 👥 Team

Built with ❤️ by **Team Kohdee** for Hackathon 2025.
Passionate about mental health, AI, and empowering healing journeys through web3.

---

## 🙏 Acknowledgments

* **Deepfunding Hackathon 2025:** For inspiring us to create CalmBot.
* **Google Gemini:** For powering empathetic responses.
* **Freesound.org:** For CC0 calming sounds.
* **U2U Network:** For enabling decentralized features and incentives.
* **Open Source Community:** Flask, p5.js, Web3.js, and more.

Let’s heal, grow, and find peace together with CalmBot 🌿
