-- 

DELETE FROM articles;

INSERT INTO articles (title, content, author_id, status, created_at, updated_at) VALUES

  --  Article 1 
  ('Containerizing a Node.js microservices architecture with Docker Compose',
   '<h2>Why Docker Compose?</h2>
<p>Docker Compose is the natural starting point for local microservice orchestration. It allows you to define multi-container applications in a single <code>docker-compose.yml</code> file, spin them up with one command, and share the configuration across your team.</p>
<blockquote>Container isolation lets each service fail independently — and recover independently.</blockquote>
<h2>Project structure</h2>
<p>We split our application into three services: <code>auth-service</code>, <code>content-service</code>, and <code>media-service</code>, each with its own Dockerfile and database volume.</p>
<h2>Health checks</h2>
<p>Every service exposes a <code>/health</code> endpoint. Docker Compose uses this to determine readiness before routing traffic.</p>',
   2, 'published',
   '2025-05-12 09:00:00', '2025-05-12 09:00:00'),

  --  Article 2 
  ('JWT authentication best practices in 2025',
   '<h2>What is a JWT?</h2>
<p>A JSON Web Token is a compact, URL-safe means of representing claims between two parties. It consists of three parts: a header, a payload, and a signature.</p>
<h2>Signing algorithms</h2>
<p>Always use asymmetric algorithms (RS256 or ES256) in production. Symmetric HS256 is fine for small projects but creates a single point of failure.</p>
<h2>Expiry and refresh tokens</h2>
<p>Short-lived access tokens (15 minutes) combined with long-lived refresh tokens stored in an HttpOnly cookie is the recommended pattern.</p>',
   3, 'published',
   '2025-04-20 11:30:00', '2025-04-20 11:30:00'),

  --  Article 3 
  ('Event-driven design with RabbitMQ and Python',
   '<h2>Why event-driven?</h2>
<p>Synchronous REST calls between services create tight coupling. When one service is slow, the caller waits. Event-driven architectures break this dependency.</p>
<h2>RabbitMQ core concepts</h2>
<p>Producers publish messages to exchanges. Exchanges route messages to queues based on binding rules. Consumers subscribe to queues and process messages asynchronously.</p>
<h2>Dead-letter queues</h2>
<p>Always configure a dead-letter exchange (DLX) to capture messages that fail processing. This prevents silent data loss.</p>',
   4, 'published',
   '2025-03-18 14:00:00', '2025-03-18 14:00:00'),

  --  Article 4 
  ('PostgreSQL indexing strategies for high-traffic APIs',
   '<h2>The default: B-tree</h2>
<p>PostgreSQL creates a B-tree index by default. It supports equality and range queries and covers most use cases.</p>
<h2>Partial indexes</h2>
<p>Index only the rows that matter. A partial index on <code>WHERE status = ''published''</code> is dramatically smaller and faster than a full-table index.</p>
<h2>GIN indexes for full-text search</h2>
<p>For <code>tsvector</code> full-text search columns, GIN indexes outperform B-tree significantly.</p>',
   2, 'published',
   '2025-02-28 08:45:00', '2025-02-28 08:45:00'),

  --  Article 5 
  ('Rate limiting at the nginx layer — a complete guide',
   '<h2>limit_req_zone</h2>
<p>Define a shared memory zone that tracks request rates per key (usually <code>$binary_remote_addr</code>). Set a rate in requests per second or minute.</p>
<h2>Burst allowance</h2>
<p>The <code>burst</code> parameter lets clients exceed the rate temporarily. Combined with <code>nodelay</code>, it absorbs traffic spikes without queuing.</p>
<h2>Per-endpoint rules</h2>
<p>Apply stricter limits to sensitive endpoints like <code>/auth/login</code> to slow brute-force attacks.</p>',
   3, 'published',
   '2025-01-15 16:20:00', '2025-01-15 16:20:00'),

  --  Article 6 (brouillon) 
  ('Building a real-time notification system with WebSockets',
   '<h2>Introduction</h2>
<p>This article is still being written. WebSockets allow bidirectional communication between client and server without polling.</p>',
   4, 'draft',
   '2025-05-10 18:00:00', '2025-05-10 18:00:00');