#!/usr/bin/env bash
set -e

# ===== 設定 =====
LABEL="P0"
FILE_TO_EDIT="main.py"         # Claude が書く先
HISTORY_DIR="claude_history"   # ログ保存先
mkdir -p "$HISTORY_DIR"

# ===== Issue 取得 =====
ISSUE_NUMBER=$(gh issue list --label "$LABEL" --state open --json number --jq '.[0].number')
if [ -z "$ISSUE_NUMBER" ]; then
  echo "★ $LABEL の open Issue がありません"; exit 0;
fi
ISSUE_TITLE=$(gh issue view "$ISSUE_NUMBER" --json title --jq '.title')
ISSUE_BODY=$(gh issue view "$ISSUE_NUMBER" --json body --jq '.body')

# ===== Claude へプロンプト =====
PROMPT="次のIssueを実装してください。\\nタイトル: ${ISSUE_TITLE}\\n本文: ${ISSUE_BODY}"
claude "$PROMPT" > "$HISTORY_DIR/issue-${ISSUE_NUMBER}.txt"

# ===== Git 操作 =====
BRANCH="issue-${ISSUE_NUMBER}"
git checkout -b "$BRANCH"
touch "$FILE_TO_EDIT"   # 無い場合は作成
cat "$HISTORY_DIR/issue-${ISSUE_NUMBER}.txt" >> "$FILE_TO_EDIT"

git add "$FILE_TO_EDIT"
git commit -m "$ISSUE_TITLE"
git push -u origin "$BRANCH"

# ===== PR 作成 =====
gh pr create --title "$ISSUE_TITLE" --body "Claude による自動実装 (#$ISSUE_NUMBER)" --head "$BRANCH"
echo "★ PR を作成しました！"

