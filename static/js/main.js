document.addEventListener("DOMContentLoaded", () => {
    const walletForm = document.getElementById("wallet-form")
    const walletAddressInput = document.getElementById("wallet-address")
    const walletInfo = document.getElementById("wallet-info")
    const loadingIndicator = document.getElementById("loading")
    const errorMessage = document.getElementById("error-message")
    const walletAddressDisplay = document.getElementById("wallet-address-display")
    const ethBalance = document.getElementById("eth-balance")
    const usdBalance = document.getElementById("usd-balance")
    const transactionsTable = document.getElementById("transactions-table")
  
    let transactionChart = null
  
    walletForm.addEventListener("submit", (e) => {
      e.preventDefault()
  
      const address = walletAddressInput.value.trim()
      if (!address) return
  
      // Show loading indicator
      walletInfo.classList.add("d-none")
      errorMessage.classList.add("d-none")
      loadingIndicator.classList.remove("d-none")
  
      // Fetch wallet data
      fetch("/api/wallet", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ address: address }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok")
          }
          return response.json()
        })
        .then((data) => {
          // Hide loading indicator
          loadingIndicator.classList.add("d-none")
  
          // Display wallet info
          displayWalletInfo(data)
  
          // Show wallet info section
          walletInfo.classList.remove("d-none")
        })
        .catch((error) => {
          // Hide loading indicator
          loadingIndicator.classList.add("d-none")
  
          // Show error message
          errorMessage.textContent = `Error: ${error.message}`
          errorMessage.classList.remove("d-none")
        })
    })

  function displayWalletInfo(data) {
    // Display wallet address
    walletAddressDisplay.textContent = data.address

    // Display balances
    ethBalance.textContent = `${data.balance.toFixed(4)} ETH`
    usdBalance.textContent = data.usd_balance ? `$${data.usd_balance.toFixed(2)}` : "N/A"

    // Display transactions
    displayTransactions(data.transactions, data.address)

    // Display chart
    displayTransactionChart(data.chart_data)
  }

  function displayTransactions(transactions, walletAddress) {
    transactionsTable.innerHTML = ""

    if (transactions.length === 0) {
      const row = document.createElement("tr")
      row.innerHTML = '<td colspan="7" class="text-center">No transactions found</td>'
      transactionsTable.appendChild(row)
      return
    }

    transactions.forEach((tx) => {
      const row = document.createElement("tr")

      // Create type cell with badge
      const typeCell = document.createElement("td")
      const typeBadge = document.createElement("span")
      typeBadge.className = `badge ${tx.type === "IN" ? "bg-success" : "bg-danger"}`
      typeBadge.textContent = tx.type
      typeCell.appendChild(typeBadge)

      // Create hash cell with link
      const hashCell = document.createElement("td")
      const hashLink = document.createElement("a")
      hashLink.href = `https://etherscan.io/tx/${tx.hash}`
      hashLink.target = "_blank"
      hashLink.className = "hash-link"
      hashLink.textContent = `${tx.hash.substring(0, 10)}...`
      hashCell.appendChild(hashLink)

      // Create from cell with address badge
      const fromCell = document.createElement("td")
      const fromBadge = document.createElement("span")
      fromBadge.className = "address-badge"
      fromBadge.title = tx.from
      fromBadge.textContent = tx.from
      fromCell.appendChild(fromBadge)

      // Create to cell with address badge
      const toCell = document.createElement("td")
      const toBadge = document.createElement("span")
      toBadge.className = "address-badge"
      toBadge.title = tx.to
      toBadge.textContent = tx.to
      toCell.appendChild(toBadge)

      row.innerHTML = `
                ${typeCell.outerHTML}
                ${hashCell.outerHTML}
                <td>${tx.date}</td>
                ${fromCell.outerHTML}
                ${toCell.outerHTML}
                <td class="${tx.type === "IN" ? "transaction-in" : "transaction-out"}">${tx.value_eth.toFixed(4)}</td>
                <td>${tx.gas_price_gwei.toFixed(2)}</td>
            `

      transactionsTable.appendChild(row)
    })
  }

  function displayTransactionChart(chartData) {
    const ctx = document.getElementById("transaction-chart").getContext("2d")

    // Destroy previous chart if it exists
    if (transactionChart) {
      transactionChart.destroy()
    }

    // Prepare data for chart
    const labels = []
    const inValues = []
    const outValues = []

    chartData.forEach((tx) => {
      const date = new Date(tx.timestamp)
      labels.push(date.toLocaleDateString())

      if (tx.type === "in") {
        inValues.push(tx.value)
        outValues.push(0)
      } else {
        inValues.push(0)
        outValues.push(tx.value)
      }
    })

    // Create new chart
    transactionChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Incoming (ETH)",
            data: inValues,
            backgroundColor: "rgba(0, 184, 148, 0.7)",
            borderColor: "rgba(0, 184, 148, 1)",
            borderWidth: 1,
          },
          {
            label: "Outgoing (ETH)",
            data: outValues,
            backgroundColor: "rgba(255, 118, 117, 0.7)",
            borderColor: "rgba(255, 118, 117, 1)",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          x: {
            stacked: true,
          },
          y: {
            stacked: true,
            beginAtZero: true,
          },
        },
      },
    })
  }
})
