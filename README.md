# Dir-Scout 🕵️‍♂️

**Dir-Scout** is a lightweight, Linux-native directory watcher that detects file system changes and sends structured messages to a **Redis Stream**. Built for developers and systems that need real-time event tracking on file activity — with minimal overhead and maximum flexibility.

---

## 🚀 Features

- Watches a directory recursively for changes (create, delete, modify, move)
- Sends events to a configurable **Redis Stream**
- Built with Docker for easy deployment
- Unix-style CLI with environment-based config
- Lightweight and reliable — perfect for pipelines, microservices, and automations

---

## 🐳 Quick Start with Docker

```bash
docker run -d \
  -e WATCH_DIR=/watched/dir \
  -e REDIS_URL=redis://your.redis.host:6379 \
  -e REDIS_STREAM=dir_events \
  -e INCLUDE_DOTFILES=false \
  -v /your/local/dir:/watched/dir \
  --name dir-scout \
  aisukezon/dir-scout
```
