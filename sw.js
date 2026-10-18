// My Trestle Board service worker.
// Network first, so brothers always get the latest version when online.
// Falls back to the last copy of the app when offline.
// Only same-origin files are cached. Sign-in and data calls (Supabase) are never touched.
const CACHE = "trestleboard-v1";
const SHELL = ["/", "/index.html", "/manifest.webmanifest", "/icons/icon-192.png", "/icons/icon-512.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  e.respondWith(
    fetch(req)
      .then(res => {
        if (res.ok && res.type === "basic") {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(req.mode === "navigate" ? "/index.html" : req, copy));
        }
        return res;
      })
      .catch(() =>
        caches.match(req.mode === "navigate" ? "/index.html" : req)
          .then(r => r || caches.match("/index.html"))
      )
  );
});
