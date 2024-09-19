const express = require('express');
const app = express();
const { exec } = require('child_process');

app.use(express.static('public'));

app.get('/cowsay/:message', (req, res) => {
  const animal = req.params.animal;
  const message = req.params.message;
  exec(`/usr/games/cowsay -f dragon ${message}`, { timeout: 5000 }, (error, stdout) => {
    if (error) return res.status(500).send("Error with cowsay command.");
    res.type('txt').send(stdout).end();
  });
});

app.listen(3000, () => {
  console.log('Server is listening on port 3000');
});
