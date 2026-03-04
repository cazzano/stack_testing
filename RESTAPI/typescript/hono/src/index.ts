import { Hono } from 'hono';
import { serve } from '@hono/node-server';

const app = new Hono();

app.get('/hello', (c) => {
  return c.text('hello');
});

const port = 3000;
console.log(`Server is running on port ${port}`);

serve({
  fetch: app.fetch,
  port
});

