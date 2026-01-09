clear

git config --global user.name "zhaopeng"
git config --global user.email "zhaopeng@neolix.ai"

git add .
git commit -m "update ${1:-auto commit}"
git push origin master