# Circle Agentic Economy — On-Chain Payment Proof

Pantheon Research completed a bounded **Circle Agent Wallet** on-chain payment proof:
founder-funded, operator-mediated, policy-limited by Circle wallet transfer caps, and
independently verified on Base.

The proof demonstrates Circle Agent Wallet usage for agentic research workflow payments while
preserving strict boundaries: **no user capital, no trading, no Pro entitlement, and no
user-payment flow.**

Machine-readable artifact: [`data/circle_agentic_payment_proof_redacted.json`](../data/circle_agentic_payment_proof_redacted.json)

---

## 1. The payment

| Field | Value |
|---|---|
| Circle product | Circle Agent Stack — Agent Wallets |
| Circle Agent Wallet | `0xaae4fab28919e5d0275fed67fca2100e0eb454bc` |
| Recipient (Pantheon-controlled) | `0x610dee1a0ec72b19c1f3cfcebab6953c49ac7470` |
| Chain | **Base mainnet** (chainId `8453`) |
| Token | USDC — `0x833589fcd6edb6e08f4c7c32d4f71b54bda02913` |
| Amount | **0.100000 USDC** (`100000` base units, 6 decimals) |
| Transaction hash | `0x699bbb9ddb03f9a98525749374fb976a9cd7ef6319414d1cb5e422d810eac6e3` |
| Block explorer | [BaseScan](https://basescan.org/tx/0x699bbb9ddb03f9a98525749374fb976a9cd7ef6319414d1cb5e422d810eac6e3) |
| Block number | `49907662` |
| Timestamp (UTC) | `2026-08-13T07:04:31Z` |
| Receipt status | `0x1` — success |
| Confirmations at verification | 56 (only grows) |
| Transfers executed | **Exactly 1** |
| Residual wallet balance | `0.000000 USDC` |

The token contract was confirmed on-chain as Circle-issued native USDC on Base
(`symbol() = "USDC"`, `decimals() = 6`) — not a bridged USDbC variant.

---

## 2. Read this before you verify — the smart-account trap

The Circle Agent Wallet is an **ERC-4337 smart account**. On the outer transaction:

- `to` is the ERC-4337 **EntryPoint** — `0x5ff137d4b0fdcd49dca30c7cf57e578a026d2789`
- `from` is a **bundler**

**Neither is the agent wallet.** A reviewer who checks the block explorer's top-level From/To will
see two unrelated addresses and reasonably conclude the proof is wrong. It is not.

The authoritative evidence is the **ERC-20 `Transfer` event log** emitted by the USDC contract
inside this transaction:

```
contract  0x833589fcd6edb6e08f4c7c32d4f71b54bda02913   (USDC on Base)
from      0xaae4fab28919e5d0275fed67fca2100e0eb454bc   (Circle Agent Wallet)
to        0x610dee1a0ec72b19c1f3cfcebab6953c49ac7470   (Pantheon recipient)
value     100000                                        (= 0.100000 USDC)
```

On BaseScan, read the **"ERC-20 Tokens Transferred"** row.

**Gas was sponsored by Circle.** The agent wallet held `0` ETH both before *and* after the
transfer — which looks impossible if you assume an ordinary EOA, and is the second tell that this
is a smart account.

---

## 3. Verify it yourself

The verification below does not depend on this repository, on Pantheon, or on any credential.
Any Base RPC endpoint will serve it.

**A. Block explorer (no tooling):** open the
[BaseScan link](https://basescan.org/tx/0x699bbb9ddb03f9a98525749374fb976a9cd7ef6319414d1cb5e422d810eac6e3)
and read the *ERC-20 Tokens Transferred* row.

**B. Raw RPC.** Substitute any public Base mainnet RPC endpoint for `<BASE_RPC_URL>`:

```bash
curl -s -X POST <BASE_RPC_URL> -H 'Content-Type: application/json' -d '{
  "jsonrpc":"2.0","id":1,"method":"eth_getTransactionReceipt",
  "params":["0x699bbb9ddb03f9a98525749374fb976a9cd7ef6319414d1cb5e422d810eac6e3"]
}' | jq '{status: .result.status, block: .result.blockNumber}'
```

Expect `status: "0x1"` and `block: "0x2f987ce"` (= 49907662).

Then decode the USDC `Transfer` log — topic `0xddf252ad…3b3ef`, sender in `topics[1]`, recipient in
`topics[2]`, value in `data`. It will show `0xaae4…54bc → 0x610d…7470`, `100000` units.

**C. Balance delta.** `balanceOf` on the recipient moved `1.000000` → `1.100000` USDC across this
block — a delta of exactly the proof amount. (The pre-existing 1.000000 USDC is unrelated to this
proof and predates it.)

**How we verified it.** We did **not** trust the Circle CLI's own output. The receipt was re-read
and the `Transfer` log decoded from raw Base RPC on **three independent public Base RPC providers**,
all agreeing, and cross-checked against the recipient balance delta.

---

## 4. Controls that were actually in force

**Circle-enforced spending policy** on the wallet, read back from the Circle CLI immediately before
the transfer:

| Limit | Value (USDC) |
|---|---|
| Per transaction | **1** |
| Daily | **2** |
| Weekly | **5** |
| Monthly | **10** |

Rule type `STABLECOIN_TRANSFER / TRANSFER_LIMIT`. The 0.10 USDC payment sits an order of magnitude
below the per-transaction ceiling.

**Founder-funded and balance-bounded.** The wallet was funded with **exactly** the proof amount,
so maximum possible exposure was 0.10 USDC. This matters more than the policy cap: the real
exposure ceiling on an agent wallet is its **balance**, not its configured limit, because
server-side controls sit on the path *to* the wallet rather than on the wallet itself.

**Human-initiated.** A human operator executed the transfer. The agent did not move money.

**Zero residual.** The transfer moved the entire balance, so the wallet holds `0.000000 USDC` and
`0` ETH. No sweep was required and no second transaction was made.

---

## 5. Honest limitations — what this proof does *not* show

These are stated plainly because a payment proof that overstates its own controls is worth less
than one that doesn't.

1. **The payment was operator-mediated.** A human ran the Circle CLI. This does **not** demonstrate
   an autonomous or recurring treasury, and the agent cannot freely spend.
2. **The production signed-in approval flow was not completed** for this proof. Pantheon's
   server-side Agent Treasury architecture — policy engine, single-use human approval gate,
   independent on-chain proof verifier, append-only ledger — exists **separately** in the private
   production system, but this final proof deliberately routed *around* it and did not exercise it.
3. **The Pantheon cloud proof verifier did not execute this payment** and has not verified it
   server-side. The verification presented here is the independent RPC/explorer verification in §3,
   which anyone can reproduce.
4. **No recipient allowlist was machine-enforced.** No Circle-side `recipient-allowlist` policy was
   configured, and no Pantheon allowlist applied. The recipient is **operator-attested** as
   Pantheon-controlled — a human claim, not a machine constraint. Risk was bounded by the
   exact-amount funding described in §4 instead.
5. **Circle's policy layer is not cryptographically proven.** The §4 limits are an operator-observed
   CLI read-back, not a chain-verifiable fact. `circle_side_policy_proven` is `false` in the
   artifact by design.

---

## 6. Non-claims

Consistent with [`safe_claims.md`](safe_claims.md), this evidence package explicitly does **not**
assert:

- ❌ a fully autonomous or recurring agent treasury
- ❌ that the agent can freely spend
- ❌ that the production signed-in approval UI was completed
- ❌ that the Pantheon cloud proof verifier executed or verified this payment
- ❌ a Circle-side or Pantheon machine-enforced recipient allowlist
- ❌ **user capital** — founder funds only, no user funds of any kind
- ❌ **trading integration** — no order path exists; LLMs never execute trades
- ❌ **Pro entitlement** — no entitlement was granted or altered
- ❌ **user-payment integration** — this is structurally separate from any user payment rail
- ❌ that this is a payment service for users
- ❌ investment advice

Payment is **not an agent-invocable tool**, so prompt injection has no path to money.

---

## 7. Why an agentic-economy payment at all

An AI research system that generates evidence packs incurs real, per-unit costs — model inference,
market data, compute. The Circle Agent Wallet is the mechanism by which such a workload can settle
those costs in USDC, programmatically and under enforceable caps, rather than through a human
expensing loop.

This proof establishes the **payment rail** end-to-end on mainnet: a Circle Agent Wallet, a live
Circle spending policy, a real USDC transfer, gas-sponsored, independently verifiable by a third
party from the public chain alone.

What it deliberately leaves unproven — autonomous initiation and the server-side approval gate that
would make autonomy safe — is exactly the part that should not be claimed before it has been
demonstrated. That gap is named in §5 rather than papered over.
