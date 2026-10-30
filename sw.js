// Coquille en cache (l'appli s'ouvre hors ligne), données toujours prises en ligne d'abord.
const CACHE = "declic-v4";
const COQUILLE = ["./", "index.html", "style.css", "app.js", "manifest.webmanifest",
  "icons/icon-180.png", "icons/icon-192.png", "icons/icon-512.png"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(COQUILLE)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys()
    .then((cles) => Promise.all(cles.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET") return;
  if (url.pathname.endsWith("data.enc.json")) {
    e.respondWith(fetch(e.request).then((rep) => {
      caches.open(CACHE).then((c) => c.put("data.enc.json", rep.clone()));
      return rep;
    }).catch(() => caches.match("data.enc.json")));
    return;
  }
  e.respondWith(caches.match(e.request).then((r) => r || fetch(e.request).then((rep) => {
    if (rep.ok && (url.origin === location.origin || url.host.includes("gstatic") || url.host.includes("googleapis"))) {
      const copie = rep.clone();
      caches.open(CACHE).then((c) => c.put(e.request, copie));
    }
    return rep;
  })));
});
