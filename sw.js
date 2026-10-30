// Toujours la dernière version en ligne d'abord ; le cache ne sert que hors ligne.
const CACHE = "declic-v11";
const COQUILLE = ["./", "index.html", "style.css", "app.js", "manifest.webmanifest",
  "icons/nitt-180.png", "icons/nitt-192.png", "icons/icon-192.png"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(COQUILLE)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys()
    .then((cles) => Promise.all(cles.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  const url = new URL(e.request.url);
  const local = url.origin === location.origin;
  const polices = url.host.includes("gstatic") || url.host.includes("googleapis");
  if (!local && !polices) return;
  if (polices) {
    e.respondWith(caches.match(e.request).then((r) => r || fetch(e.request).then((rep) => {
      const copie = rep.clone();
      caches.open(CACHE).then((c) => c.put(e.request, copie));
      return rep;
    })));
    return;
  }
  const cle = url.pathname.endsWith(".enc.json") ? url.pathname : e.request;
  e.respondWith(fetch(e.request, { cache: "no-store" }).then((rep) => {
    if (rep.ok) { const copie = rep.clone(); caches.open(CACHE).then((c) => c.put(cle, copie)); }
    return rep;
  }).catch(() => caches.match(cle, { ignoreSearch: true })));
});
