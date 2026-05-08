# ✅ Pre-Launch Checklist

## 🔧 Setup & Installation

- [ ] Python 3.8+ is installed
- [ ] Project folder location: `C:\AYUSH\openeyes\production-ai-agent\`
- [ ] Virtual environment created (optional but recommended)
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] No errors during pip install

## 🔑 Configuration

- [ ] `.env` file created from `.env.example`
- [ ] `GROQ_API_KEY` added to `.env`
- [ ] `GROQ_MODEL` set in `.env` (default: llama-3.3-70b-versatile)
- [ ] `GOOGLE_API_KEY` added to `.env`
- [ ] `PINECONE_API_KEY` added to `.env`
- [ ] `PINECONE_INDEX` added to `.env`
- [ ] `.env` file is in `.gitignore` (security)

## 📁 Project Structure

- [ ] `streamlit_app.py` exists
- [ ] `run.py` exists
- [ ] `.streamlit/config.toml` exists
- [ ] `agent/agent.py` exists
- [ ] `retriever.py` exists
- [ ] `memory.py` exists
- [ ] `.env` file exists

## 📚 Data Preparation (if using RAG)

- [ ] PDFs added to `data/` folder
- [ ] `python ingest.py` executed successfully
- [ ] No errors during document processing
- [ ] `storage/chunks.pkl` created
- [ ] `memory.db` created (will be auto-created on first run)

## ✅ Pre-Flight Checks

Run the verification script:
```bash
python verify.py
```

All checks should show ✅:
- [ ] Python Version
- [ ] Environment File
- [ ] Dependencies
- [ ] Project Structure
- [ ] Data Directory
- [ ] Processed Chunks

## 🚀 Launch

```bash
python run.py
```

- [ ] No error messages in terminal
- [ ] Terminal shows: `Streamlit app is running at http://localhost:8501`
- [ ] Browser opens automatically (or manually go to that URL)
- [ ] UI loads without errors

## 🧪 Functionality Test

### RAG Mode Test
- [ ] Select "RAG" from mode dropdown
- [ ] Type a test question: "What documents do you have?"
- [ ] Wait for response
- [ ] Response appears in chat
- [ ] Response is saved to chat history

### Agent Mode Test
- [ ] Select "Agent" from mode dropdown
- [ ] Type a test question: "Hello, can you help me?"
- [ ] Wait for response
- [ ] Response appears in chat
- [ ] Response is saved to chat history

### Thinking Toggle Test
- [ ] Check "Show Thinking" checkbox
- [ ] Send a message
- [ ] See "🔍 Retrieving documents..." or "💭 Agent is thinking..."
- [ ] Thinking message disappears after response
- [ ] Uncheck "Show Thinking"
- [ ] Send another message
- [ ] No thinking messages appear

### Chat History Test
- [ ] Send multiple messages
- [ ] All previous messages remain visible
- [ ] Chat history persists
- [ ] Click "Clear Chat"
- [ ] All messages disappear
- [ ] Send new message
- [ ] New session starts clean

### Session Management Test
- [ ] Check sidebar for session ID
- [ ] Session ID is unique per app start
- [ ] Close and reopen browser
- [ ] Session memory is loaded
- [ ] Previous messages appear again

## 🛠️ Troubleshooting Checklist

If something isn't working:

- [ ] Check terminal for error messages
- [ ] Run `python verify.py` to identify issues
- [ ] Verify `.env` file has all required keys
- [ ] Check API keys are correct and valid
- [ ] Ensure internet connection is stable
- [ ] Try restarting the app: `python run.py`
- [ ] Check Python version: `python --version`
- [ ] Reinstall dependencies: `pip install -r requirements.txt --upgrade`

## 📝 Notes for Deployment

- [ ] `.env` file will not be committed to git
- [ ] `memory.db` stores chat history (back this up if needed)
- [ ] `storage/chunks.pkl` contains processed documents
- [ ] Streamlit app runs on port 8501 by default
- [ ] App is single-user (for production, use deployment platform)

## 🎉 Ready to Deploy?

If all checkboxes are ✅, you're ready to:

1. **Run locally:**
   ```bash
   python run.py
   ```

2. **Deploy to cloud** (optional):
   - Streamlit Cloud: https://streamlit.io/cloud
   - Heroku: https://www.heroku.com
   - AWS: https://aws.amazon.com
   - Google Cloud: https://cloud.google.com

---

## 📞 Quick Reference

| Command | Purpose |
|---------|---------|
| `python verify.py` | Check setup |
| `python ingest.py` | Process documents |
| `python run.py` | Start the app |
| `streamlit run streamlit_app.py` | Alternative start |
| `pip install -r requirements.txt` | Install dependencies |

---

## ⚠️ Common Issues & Solutions

### App won't start
- Check error message in terminal
- Run `python verify.py`
- Ensure `.env` is configured

### No responses from AI
- Check API keys in `.env`
- Verify internet connection
- Check API rate limits

### RAG mode not working
- Ensure `ingest.py` was run
- Check `storage/chunks.pkl` exists
- Verify PDFs are in `data/` folder

### Chat history not saving
- Check `memory.db` exists
- Verify database permissions
- Check disk space available

---

**Status**: Ready for Launch ✨  
**Last Updated**: 2024  
**Support**: Check SETUP_GUIDE.md for detailed help
