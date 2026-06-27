'use strict';

/**
 * AI Cooking To-Do List — Frontend Application
 *
 * Handles form submission, API communication, and dynamic
 * rendering of meal plans, grocery lists, substitutions, and
 * budget breakdowns.
 */

document.addEventListener('DOMContentLoaded', () => {
  // ─── DOM References (getElementById for perf) ───
  const form              = document.getElementById('meal-plan-form');
  const submitBtn         = document.getElementById('submit-btn');
  const dayContext        = document.getElementById('day-context');
  const dayContextCount   = document.getElementById('day-context-count');
  const dietaryPrefs      = document.getElementById('dietary-preferences');
  const budgetInput       = document.getElementById('budget');
  const numPeopleInput    = document.getElementById('num-people');
  const errorMessage      = document.getElementById('error-message');
  const errorText         = document.getElementById('error-text');
  const errorDismiss      = document.getElementById('error-dismiss');
  const resultsContainer  = document.getElementById('results-container');
  const mealPlanCards     = document.getElementById('meal-plan-cards');
  const groceryTableBody  = document.getElementById('grocery-table-body');
  const subsSection       = document.getElementById('substitutions-section');
  const subsCards         = document.getElementById('substitutions-cards');
  const budgetBreakdown   = document.getElementById('budget-breakdown');

  // ─── Character Counter ───
  dayContext.addEventListener('input', () => {
    dayContextCount.textContent = dayContext.value.length;
  });

  // ─── Error Dismiss ───
  errorDismiss.addEventListener('click', () => hideElement('error-message'));

  // ─── Keyboard Shortcut: Ctrl+Enter to submit ───
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      form.requestSubmit();
    }
  });

  // ─── Form Submission ───
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    hideElement('error-message');
    hideElement('results-container');

    // Validate
    const context = dayContext.value.trim();
    const budget  = parseFloat(budgetInput.value);
    const people  = parseInt(numPeopleInput.value, 10);

    if (!context) {
      showError('Please describe your day so we can plan meals for you.');
      dayContext.focus();
      return;
    }

    if (isNaN(budget) || budget <= 0) {
      showError('Please enter a valid budget greater than ₹0.');
      budgetInput.focus();
      return;
    }

    if (isNaN(people) || people < 1 || people > 20) {
      showError('Number of people must be between 1 and 20.');
      numPeopleInput.focus();
      return;
    }

    // Build payload
    const payload = {
      day_context: context,
      dietary_preferences: dietaryPrefs.value.trim(),
      budget: budget,
      num_people: people,
    };

    setLoading(true);

    try {
      const data = await fetchMealPlan(payload);
      renderResults(data);
    } catch (err) {
      showError(err.message || 'An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  });


  // ═══════════════════════════════════════════════════════
  //  API Communication
  // ═══════════════════════════════════════════════════════

  /**
   * Sends a POST request to the meal plan API with a 30-second timeout.
   *
   * @param {Object} payload - The request body conforming to the API contract.
   * @returns {Promise<Object>} Parsed JSON response.
   * @throws {Error} On network failure, timeout, or non-OK status.
   */
  async function fetchMealPlan(payload) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000);

    try {
      const response = await fetch('/api/generate-meal-plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        let msg = `Server error (${response.status})`;
        try {
          const errBody = await response.json();
          if (errBody.detail) msg = errBody.detail;
          if (errBody.error) msg = errBody.error;
        } catch { /* ignore parse errors */ }
        throw new Error(msg);
      }

      const data = await response.json();

      if (!data.meals || !Array.isArray(data.meals)) {
        throw new Error('Received an unexpected response format. Please try again.');
      }

      return data;
    } catch (err) {
      clearTimeout(timeoutId);
      if (err.name === 'AbortError') {
        throw new Error('Request timed out after 30 seconds. Please try again.');
      }
      throw err;
    }
  }


  // ═══════════════════════════════════════════════════════
  //  Rendering
  // ═══════════════════════════════════════════════════════

  /**
   * Orchestrates rendering of all result sections and scrolls to them.
   *
   * @param {Object} data - The full API response object.
   */
  function renderResults(data) {
    renderMealPlan(data.meals || []);
    renderGroceryList(data.grocery_list || []);
    renderSubstitutions(data.substitutions || []);
    renderBudgetBreakdown(data.budget_breakdown || null);

    showElement('results-container');

    // Smooth scroll to results
    setTimeout(() => {
      resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
  }

  /**
   * Renders meal plan cards for each meal.
   *
   * @param {Array<Object>} meals - Array of meal objects from the API.
   */
  function renderMealPlan(meals) {
    if (meals.length === 0) {
      mealPlanCards.innerHTML = `<p style="color:var(--clr-text-muted)">No meals generated.</p>`;
      return;
    }

    const mealTypeIcons = {
      breakfast: '🌅',
      lunch:     '☀️',
      dinner:    '🌙',
      snack:     '🍿',
    };

    mealPlanCards.innerHTML = meals.map((meal, i) => {
      const icon = mealTypeIcons[meal.meal_type?.toLowerCase()] || '🍽️';
      const ingredients = (meal.ingredients || [])
        .map(ing => `<li class="meal-card__ingredient">${sanitizeHTML(ing)}</li>`)
        .join('');

      return `
        <article class="meal-card glass-card" role="listitem" style="animation-delay:${i * 80}ms">
          <div class="meal-card__header">
            <span class="meal-card__type">${icon} ${sanitizeHTML(meal.meal_type || 'Meal')}</span>
            <span class="meal-card__prep">⏱ ${sanitizeHTML(String(meal.prep_time_minutes ?? '—'))} min</span>
          </div>
          <h3 class="meal-card__name">${sanitizeHTML(meal.dish_name || 'Untitled Dish')}</h3>
          <p class="meal-card__desc">${sanitizeHTML(meal.description || '')}</p>
          <p class="meal-card__ingredients-title">Ingredients</p>
          <ul class="meal-card__ingredients">${ingredients || '<li class="meal-card__ingredient">—</li>'}</ul>
        </article>`;
    }).join('');
  }

  /**
   * Renders the grocery list as a table.
   *
   * @param {Array<Object>} items - Array of grocery item objects.
   */
  function renderGroceryList(items) {
    if (items.length === 0) {
      groceryTableBody.innerHTML = `
        <tr><td colspan="4" style="text-align:center;color:var(--clr-text-dim)">No grocery items.</td></tr>`;
      return;
    }

    groceryTableBody.innerHTML = items.map(item => `
      <tr>
        <td>${sanitizeHTML(item.name || '—')}</td>
        <td>${sanitizeHTML(item.quantity || '—')}</td>
        <td class="cost-cell">${formatCurrency(item.estimated_cost)}</td>
        <td><span class="category-badge">${sanitizeHTML(item.category || '—')}</span></td>
      </tr>`).join('');
  }

  /**
   * Renders substitution suggestion cards.
   * Hides the section entirely if there are no substitutions.
   *
   * @param {Array<Object>} subs - Array of substitution objects.
   */
  function renderSubstitutions(subs) {
    if (!subs || subs.length === 0) {
      hideElement('substitutions-section');
      return;
    }

    showElement('substitutions-section');

    subsCards.innerHTML = subs.map((sub, i) => `
      <div class="sub-card glass-card" role="listitem" style="animation-delay:${i * 60}ms">
        <div class="sub-card__flow">
          <span class="sub-card__original">${sanitizeHTML(sub.original || '—')}</span>
          <span class="sub-card__arrow" aria-hidden="true">→</span>
          <span class="sub-card__substitute">${sanitizeHTML(sub.substitute || '—')}</span>
          ${sub.reason ? `<p class="sub-card__reason">${sanitizeHTML(sub.reason)}</p>` : ''}
        </div>
      </div>`).join('');
  }

  /**
   * Renders the budget breakdown with a progress bar and savings tips.
   *
   * @param {Object|null} budget - Budget breakdown object from the API.
   */
  function renderBudgetBreakdown(budget) {
    if (!budget) {
      budgetBreakdown.innerHTML = `<p style="color:var(--clr-text-dim)">No budget data available.</p>`;
      return;
    }

    const total     = budget.total_estimated_cost ?? 0;
    const cap       = budget.budget ?? 1;
    const withinBudget = budget.is_within_budget !== false;
    const pct       = Math.min((total / cap) * 100, 100);
    const tips      = budget.savings_tips || [];

    const statusClass = withinBudget ? 'budget-status--ok' : 'budget-status--over';
    const statusText  = withinBudget ? '✅ Within budget' : '⚠️ Over budget';
    const barClass    = withinBudget ? '' : 'progress-fill--over';

    const tipsHTML = tips.length > 0 ? `
      <h4 class="tips-title">💡 Savings Tips</h4>
      <ul class="tips-list">
        ${tips.map(tip => `<li>${sanitizeHTML(tip)}</li>`).join('')}
      </ul>` : '';

    budgetBreakdown.innerHTML = `
      <div class="budget-summary">
        <div>
          <span class="budget-label">Estimated Total</span>
          <p class="budget-amount">${formatCurrency(total)}</p>
        </div>
        <span class="budget-of">of ${formatCurrency(cap)} budget</span>
      </div>
      <div class="progress-track" role="progressbar" aria-valuenow="${Math.round(pct)}" aria-valuemin="0" aria-valuemax="100" aria-label="Budget usage">
        <div class="progress-fill ${barClass}" style="width:0%"></div>
      </div>
      <span class="${statusClass} budget-status">${statusText}</span>
      ${tipsHTML}`;

    // Animate progress bar after DOM paint
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        const fill = budgetBreakdown.querySelector('.progress-fill');
        if (fill) fill.style.width = `${pct}%`;
      });
    });
  }


  // ═══════════════════════════════════════════════════════
  //  Helpers
  // ═══════════════════════════════════════════════════════

  /**
   * Shows a DOM element by removing the `hidden` attribute.
   *
   * @param {string} id - The element's ID.
   */
  function showElement(id) {
    const el = document.getElementById(id);
    if (el) el.removeAttribute('hidden');
  }

  /**
   * Hides a DOM element by setting the `hidden` attribute.
   *
   * @param {string} id - The element's ID.
   */
  function hideElement(id) {
    const el = document.getElementById(id);
    if (el) el.setAttribute('hidden', '');
  }

  /**
   * Formats a numeric amount as Indian Rupees.
   *
   * @param {number|string} amount - The monetary value.
   * @returns {string} Formatted string, e.g. "₹450.00".
   */
  function formatCurrency(amount) {
    const num = parseFloat(amount);
    if (isNaN(num)) return '₹0.00';
    return `₹${num.toFixed(2)}`;
  }

  /**
   * Escapes HTML entities to prevent XSS when inserting
   * user-generated or API-sourced content into the DOM.
   *
   * @param {string} str - Raw string to sanitize.
   * @returns {string} HTML-escaped string.
   */
  function sanitizeHTML(str) {
    if (typeof str !== 'string') return '';
    const map = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;',
    };
    return str.replace(/[&<>"']/g, (char) => map[char]);
  }

  /**
   * Displays an error message to the user.
   *
   * @param {string} message - Error message to display.
   */
  function showError(message) {
    errorText.textContent = message;
    showElement('error-message');
    errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  /**
   * Toggles the loading state on the submit button.
   *
   * @param {boolean} isLoading - Whether to show the loading state.
   */
  function setLoading(isLoading) {
    if (isLoading) {
      submitBtn.classList.add('is-loading');
      submitBtn.setAttribute('aria-busy', 'true');
      submitBtn.disabled = true;
    } else {
      submitBtn.classList.remove('is-loading');
      submitBtn.removeAttribute('aria-busy');
      submitBtn.disabled = false;
    }
  }
});
