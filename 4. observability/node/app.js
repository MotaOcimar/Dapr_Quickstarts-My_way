// ------------------------------------------------------------
// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.
// ------------------------------------------------------------

const express = require('express');
const bodyParser = require('body-parser');
require('isomorphic-fetch');
const app = express();
app.use(bodyParser.json());
const cors = require('cors');
const port = 4000;

app.use(cors());

app.post('/divide', (req, res) => {
  //////////////////////////
  // Adicionando uma chamada externa para verificar se o tracing depende do sidecar Dapr
  baconipsun = "https://baconipsum.com/api/?type=meat-and-filler&sentences=1";
  fetch(baconipsun)
  .then(resp => resp.json())
  .then(json => {
      console.log(json);
  });
  //////////////////////////


  let args = req.body;
  const [operandOne, operandTwo] = [Number(args['operandOne']), Number(args['operandTwo'])];
  
  console.log(`Dividing ${operandOne} by ${operandTwo}`);
  
  let result = operandOne / operandTwo;
  res.send(result.toString());
});

app.listen(port, () => console.log(`Listening on port ${port}!`));