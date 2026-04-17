/**
 * HRMS Chatbot - Polished UI with chat history.
 * Persists history to localStorage; sends history to API for context.
 * Renders assistant replies with markdown-style formatting (tables, bold, lists).
 */
(function () {
  // History is now kept only in-memory per open session (no localStorage),
  // so chats are not shared between different users on the same machine.
  const MAX_HISTORY = 50;
  const API_URL = '/chatbot/api/chat';

  const widget = document.getElementById('hrms-chatbot-widget');
  const toggle = document.getElementById('hrms-chatbot-toggle');
  const panel = document.getElementById('hrms-chatbot-panel');
  const messagesEl = document.getElementById('hrms-chatbot-messages');
  const form = document.getElementById('hrms-chatbot-form');
  const input = document.getElementById('hrms-chatbot-input');
  const sendBtn = document.getElementById('hrms-chatbot-send');
  const closeBtn = document.querySelector('.hrms-chatbot-close');

  let history = [];

  const SUGGESTED_QUERIES = [
    {
      label: 'CO dashboard summary',
      text: 'Show full CO dashboard summary with detachments, manpower, interviews, loans, courses, projects, sensitive individuals, roll call points and agniveers.',
    },
    {
      label: 'Current manpower',
      text: 'What is the current manpower breakdown on the CO dashboard (officers, JCOs and ORs)?',
    },
    {
      label: 'Detachments',
      text: 'On the CO dashboard, how many personnel are currently on detachment?',
    },
    {
      label: 'TD / Attachment',
      text: 'On the CO dashboard, how many personnel are on TD / attachment?',
    },
    {
      label: 'Sensitive individuals',
      text: 'On the CO dashboard, how many sensitive individuals are marked?',
    },
    {
      label: 'Loans & projects',
      text: 'On the CO dashboard, how many active loans and how many projects are there?',
    },
    {
      label: 'Roll call points',
      text: 'On the CO dashboard, how many roll call points are pending?',
    },
    {
      label: 'My pending tasks',
      text: 'On the CO dashboard, what is my task summary (total tasks and pending tasks)?',
    },
    {
      label: 'Agniveer strength',
      text: 'On the CO dashboard, how many Agniveers are there?',
    },
  ];

  function loadHistory() {
    // No-op: we no longer restore history from localStorage to avoid
    // leaking conversations between different logged-in users.
    history = [];
  }

  function saveHistory() {
    // No-op: history is kept only for the current open panel.
  }

  /**
   * Simple markdown-style render: **bold**, | table |, bullet lists.
   * Returns safe HTML (escaped except for allowed tags).
   */
  function renderMarkdown(text) {
    if (!text || typeof text !== 'string') return '';
    const lines = text.split('\n');
    const out = [];
    let i = 0;
    while (i < lines.length) {
      const line = lines[i];
      const isTableRow = /^\|.+\|$/.test(line);
      const isSepRow = /^\|[\s\-:|]+\|$/.test(line);
      if (isTableRow) {
        const tableLines = [];
        while (i < lines.length && /^\|.+\|$/.test(lines[i])) {
          var row = lines[i];
          if (!/^\|[\s\-:|]+\|$/.test(row)) {
            tableLines.push(row);
          }
          i++;
        }
        if (tableLines.length) {
          const header = tableLines[0];
          const body = tableLines.slice(1);
          const toCell = function (raw, isTh) {
            const tag = isTh ? 'th' : 'td';
            const content = escapeHtml(raw.trim());
            return '<' + tag + '>' + content + '</' + tag + '>';
          };
          const headerCells = header.split('|').slice(1, -1).map(function (c) { return toCell(c, true); });
          const headerHtml = '<tr>' + headerCells.join('') + '</tr>';
          const bodyHtml = body.map(function (row) {
            const cells = row.split('|').slice(1, -1).map(function (c) { return toCell(c, false); });
            return '<tr>' + cells.join('') + '</tr>';
          }).join('');
          out.push('<div class="hrms-chat-table-wrap"><table class="hrms-chat-table"><thead>' + headerHtml + '</thead><tbody>' + bodyHtml + '</tbody></table></div>');
        }
        continue;
      }
      let escaped = escapeHtml(line);
      escaped = escaped.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
      escaped = escaped.replace(/\*([^*]+)\*/g, '<em>$1</em>');
      if (/^[•\-]\s+/.test(line)) {
        out.push('<div class="hrms-chat-bullet">' + escaped.replace(/^[•\-]\s+/, '') + '</div>');
      } else if (escaped.trim()) {
        out.push(escaped);
      } else {
        out.push('<br>');
      }
      i++;
    }
    return out.join('<br>');
  }

  function escapeHtml(s) {
    const div = document.createElement('div');
    div.textContent = s;
    return div.innerHTML;
  }

  function addMessage(role, content, options) {
    const id = 'msg-' + Date.now() + '-' + Math.random().toString(36).slice(2, 6);
    const bubble = document.createElement('div');
    bubble.className = 'hrms-chat-bubble hrms-chat-bubble--' + role;
    bubble.setAttribute('data-role', role);
    bubble.id = id;

    const inner = document.createElement('div');
    inner.className = 'hrms-chat-bubble-inner';
    if (role === 'assistant') {
      inner.className += ' hrms-chat-reply';
      inner.innerHTML = renderMarkdown(content);
    } else {
      inner.textContent = content;
    }
    bubble.appendChild(inner);
    if (options && options.loading) {
      bubble.classList.add('hrms-chat-bubble--loading');
    }
    messagesEl.appendChild(bubble);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return bubble;
  }

  function setBubbleContent(bubble, content) {
    const inner = bubble.querySelector('.hrms-chat-bubble-inner');
    if (!inner) return;
    inner.innerHTML = renderMarkdown(content);
    bubble.classList.remove('hrms-chat-bubble--loading');
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function renderHistory() {
    // Initial welcome view (fresh chat every time panel is opened/reset)
    messagesEl.innerHTML = '';
    addMessage(
      'assistant',
      "Hi! I'm your HRMS assistant. Ask me **any** question about this project or the database—e.g. leave workflow, personnel table, weight system, tasks, loans, or schema.\n\nYou can also tap one of these common CO dashboard questions:"
    );
    renderSuggestions();
  }

  function pushToHistory(role, content) {
    history.push({ role: role, content: content });
    saveHistory();
  }

  function getHistoryForApi() {
    return history.map(function (e) {
      return { role: e.role, content: e.content };
    });
  }

  function setLoading(loading) {
    if (sendBtn) sendBtn.disabled = loading;
    if (input) input.disabled = loading;
  }

  function submitMessage(textOverride) {
    const text = (textOverride || (input && input.value) || '').trim();
    if (!text) return;
    if (!textOverride && input) input.value = '';
    addMessage('user', text);
    pushToHistory('user', text);

    const bubble = addMessage('assistant', '…', { loading: true });
    setLoading(true);

    fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: text,
        history: getHistoryForApi().slice(0, -1)
      }),
      credentials: 'same-origin'
    })
      .then(function (res) {
        return res.json().then(function (data) {
          if (!res.ok) throw new Error(data.error || 'Request failed');
          return data;
        });
      })
      .then(function (data) {
        const reply = (data.reply != null ? data.reply : 'No response.');
        setBubbleContent(bubble, reply);
        pushToHistory('assistant', reply);
      })
      .catch(function (err) {
        const msg = err.message || 'Something went wrong. Please try again.';
        setBubbleContent(bubble, '**Error:** ' + msg);
        pushToHistory('assistant', '**Error:** ' + msg);
      })
      .finally(function () {
        setLoading(false);
      });
  }

  function renderSuggestions() {
    if (!messagesEl) return;
    const wrap = document.createElement('div');
    wrap.className = 'hrms-chat-suggestions';
    SUGGESTED_QUERIES.forEach(function (q) {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'hrms-chat-suggestions-btn';
      btn.textContent = q.label;
      btn.addEventListener('click', function () {
        submitMessage(q.text);
      });
      wrap.appendChild(btn);
    });
    messagesEl.appendChild(wrap);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      submitMessage();
    });
  }
  if (input) {
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        submitMessage();
      }
    });
  }
  if (toggle) {
    toggle.addEventListener('click', function () {
      const willOpen = !panel.classList.contains('hrms-chat-panel--open');
      panel.classList.toggle('hrms-chat-panel--open');
      toggle.setAttribute('aria-expanded', panel.classList.contains('hrms-chat-panel--open'));
      if (willOpen) {
        // Fresh chat UI every time the panel is opened
        history = [];
        if (messagesEl) {
          renderHistory();
        }
        input && input.focus();
      }
    });
  }
  if (closeBtn) {
    closeBtn.addEventListener('click', function () {
      panel.classList.remove('hrms-chat-panel--open');
      toggle && toggle.setAttribute('aria-expanded', 'false');
      // Clear current session when user explicitly closes the chatbot
      history = [];
      if (messagesEl) {
        messagesEl.innerHTML = '';
      }
    });
  }

  if (messagesEl) {
    // On first load, show a clean welcome (no previous messages).
    loadHistory();
    renderHistory();
  }
})();
