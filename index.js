const express = require('express');
const app = express();
const { exec } = require('child_process');

app.use(express.static('public'));

// URL: /cowsay/:animal/:message
app.get('/cowsay/:animal/:message', (req, res) => {
  const animal = req.params.animal;    // 動物の種類（カスタムキャラクター含む）を取得
  const message = req.params.message;  // メッセージを取得
  exec(`/usr/games/cowsay -f ${animal} -f ${message}`, { timeout: 5000 }, (error, stdout) => {
    if (error) return res.status(500).send("Error with cowsay command.");
    res.type('txt').send(stdout).end();
  });
});

app.listen(3000, () => {
  console.log('Server is listening on port 3000');
});
