// Executes the real middleware.js with Web Request objects. Does NOT prove a Vercel deployment is protected (see verify_deploy.sh).
import assert from "node:assert";
const run = async (env, auth) => { for (const k of ["DASHBOARD_USER","DASHBOARD_PASS","ACCESS_MODE"]) delete process.env[k]; Object.assign(process.env, env);
  const m = await import("../middleware.js?" + Math.random()); const r = m.default(new Request("https://x.test/", { headers: auth ? { authorization: auth } : {} })); return r; };
const b = (u, p) => "Basic " + Buffer.from(u + ":" + p).toString("base64"); let n = 0;
const t = async (name, fn) => { await fn(); n++; console.log("PASS", name); };
await t("missing credentials fails closed (503)", async () => assert.equal((await run({}, null)).status, 503));
await t("missing credentials + valid-looking auth still 503", async () => assert.equal((await run({}, b("a","b"))).status, 503));
await t("ACCESS_MODE=open explicitly allows", async () => assert.notEqual((await run({ ACCESS_MODE: "open" }, null)).status, 503));
await t("configured, no auth header -> 401 + challenge", async () => { const r = await run({ DASHBOARD_USER: "u", DASHBOARD_PASS: "p" }, null); assert.equal(r.status, 401); assert.ok(r.headers.get("www-authenticate")); });
await t("wrong password -> 401", async () => assert.equal((await run({ DASHBOARD_USER: "u", DASHBOARD_PASS: "p" }, b("u","x"))).status, 401));
await t("wrong user -> 401", async () => assert.equal((await run({ DASHBOARD_USER: "u", DASHBOARD_PASS: "p" }, b("x","p"))).status, 401));
await t("malformed header -> 401", async () => assert.equal((await run({ DASHBOARD_USER: "u", DASHBOARD_PASS: "p" }, "Basic %%%")).status, 401));
await t("password containing a colon works", async () => assert.notEqual((await run({ DASHBOARD_USER: "u", DASHBOARD_PASS: "p:q" }, b("u","p:q"))).status, 401));
await t("correct credentials pass through", async () => { const r = await run({ DASHBOARD_USER: "u", DASHBOARD_PASS: "p" }, b("u","p")); assert.notEqual(r.status, 401); assert.notEqual(r.status, 503); });
console.log("TOTAL", n, "/ 9");
