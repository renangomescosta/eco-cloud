import express from "express";

type Usuario = { id: number; nome: string };
let contagemDeRequisicoes = 0;

const app = express();
const PORT = 3000;

app.use(express.json());

let usuarioAtual: Usuario | null = null;

app.get("/usuario", (req, res) => {
  contagemDeRequisicoes+=1;
  if (!usuarioAtual) return res.status(404).json({ erro: "Nenhum usuário definido" });
  res.json(usuarioAtual);
});

app.post("/usuario", (req, res) => {
  contagemDeRequisicoes+=1;

  const { id, nome } = req.body ?? {};

  if (typeof id !== "number" || typeof nome !== "string") {
    return res.status(400).json({ erro: "Envie 'id' (número) e 'nome' (texto)" });
  }

  usuarioAtual = { id, nome };
  res.status(201).json(usuarioAtual);
});

app.get("/contagem", (req, res) => {
  return res.status(200).json({contagem:contagemDeRequisicoes});
});

const server = app.listen(PORT, () => console.log(`http://localhost:${PORT}`));

process.on("SIGTERM", () => server.close(() => process.exit(0)));