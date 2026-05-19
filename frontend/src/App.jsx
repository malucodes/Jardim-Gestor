import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [sementes, setSementes] = useState([])
  const [nomeNovaSemente, setNomeNovaSemente] = useState('')

  const carregarJardim = async () => {
    try {
      const resposta = await fetch('http://localhost:8000/canteiros')
      const dados = await resposta.json()
      setSementes(dados.sementes)
    } catch (erro) {
      console.error("Erro ao conectar com a API:", erro)
    }
  }

  const plantarSemente = async (evento) => {
    evento.preventDefault()
    if (!nomeNovaSemente.trim()) return

    try {
      await fetch('http://localhost:8000/plantar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome: nomeNovaSemente })
      })
      setNomeNovaSemente('')
      carregarJardim()
    } catch (erro) {
      console.error("Erro ao plantar:", erro)
    }
  }

  // NOVA FUNÇÃO: Atualizar o status (Regar)
  const regarSemente = async (nome, statusAtual) => {
    try {
      // O encodeURIComponent garante que nomes com espaço (ex: "Estudar Python") funcionem na URL
      await fetch(`http://localhost:8000/cuidar/${encodeURIComponent(nome)}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        // Inverte o status atual: se era false (não concluído), vira true, e vice-versa
        body: JSON.stringify({ novo_status: !statusAtual })
      })
      carregarJardim() // Recarrega para mostrar a florzinha!
    } catch (erro) {
      console.error("Erro ao regar:", erro)
    }
  }

  // NOVA FUNÇÃO: Deletar (Podar)
  const podarSemente = async (nome) => {
    try {
      await fetch(`http://localhost:8000/podar/${encodeURIComponent(nome)}`, {
        method: 'DELETE'
      })
      carregarJardim() // Recarrega para remover da tela
    } catch (erro) {
      console.error("Erro ao podar:", erro)
    }
  }

  useEffect(() => {
    carregarJardim()
  }, [])

  return (
      <div className="jardim-container">
        <header>
          <h1>✨ Meu Jardim Virtual 🎀</h1>
          <p>Cultivando minha rotina, uma semente de cada vez.</p>
        </header>

        <form onSubmit={plantarSemente} className="formulario-plantio">
          <input
              type="text"
              className="input-semente"
              placeholder="O que vamos cultivar hoje?..."
              value={nomeNovaSemente}
              onChange={(e) => setNomeNovaSemente(e.target.value)}
          />
          <button type="submit" className="btn-plantar">
            Plantar 🌷
          </button>
        </form>

        <main className="canteiro">
          {sementes.length === 0 ? (
              <p className="aviso">O solo está livre! Que tal plantar a primeira semente?</p>
          ) : (
              sementes.map((semente, index) => (
                  <div key={index} className={`card-semente ${semente.concluido ? 'floresceu' : ''}`}>
                    <h2>{semente.nome}</h2>
                    <div className="status-badge">
                      {semente.concluido ? '🌸 Floresceu' : '🌿 Crescendo'}
                    </div>

                    {/* NOVOS BOTÕES: Ações de cada planta */}
                    <div className="acoes-card">
                      <button
                          onClick={() => regarSemente(semente.nome, semente.concluido)}
                          className="btn-regar"
                      >
                        {semente.concluido ? 'Desfazer 🔄' : 'Regar 💧'}
                      </button>

                      <button
                          onClick={() => podarSemente(semente.nome)}
                          className="btn-podar"
                      >
                        Podar ✂️
                      </button>
                    </div>
                  </div>
              ))
          )}
        </main>
      </div>
  )
}

export default App