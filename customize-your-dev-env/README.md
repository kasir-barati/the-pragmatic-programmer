# Customize your Dev Env

```bash
alias dcps='docker compose ps --format "table {{.Service}}\t{{.Status}}\t{{.Ports}}"'
alias dcd='docker compose down -v'
alias dcu='docker compose up --build -d'
```
