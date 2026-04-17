const showLoader = (id, show) => {
  document.getElementById(id).style.display = show ? "flex" : "none";
};

let fitCount = 0;
let unFitCount = 0;
let safeCount = 0;
let categoryCount = 0;
let currentCompany = "All";
let tableData = [];
let displayedData = [];
let currentStatusClass = "";
let currentPage = 1;
let isLoading = false;
let hasMoreData = true;
const rowsPerPage = 10;

// Validation popup functions
function showValidationPopup(message) {
  const popup = document.getElementById('validation-popup');
  const messageEl = document.getElementById('validation-message');
  messageEl.textContent = message;
  popup.style.display = 'flex';
}

function closeValidationPopup() {
  const popup = document.getElementById('validation-popup');
  popup.style.display = 'none';
}

async function loadCompanies() {
  try {
      // Get logged-in user's company and username
      let userCompany = null;
      let username = null;
      try {
          const userRes = await fetch("/api/user-info");
          if (userRes.ok) {
              const userData = await userRes.json();
              if (userData.success) {
                  userCompany = userData.company;
                  username = userData.username;
              }
          }
      } catch (e) {
          console.warn("Could not fetch user info:", e);
      }
      
      // Fallback: Try to get from template variable if available
      if (!userCompany && typeof window.userCompanyFromTemplate !== 'undefined' && window.userCompanyFromTemplate) {
          userCompany = window.userCompanyFromTemplate;
      }
      
      const companySelect = document.getElementById("company-select");
      while (companySelect.options.length > 1) {
          companySelect.remove(1);
      }
      
      // Normalize company name for matching
      const normalizeCompany = (comp) => {
          if (!comp) return null;
          const lower = comp.toLowerCase().trim();
          if (lower.includes('1') && (lower.includes('company') || lower.includes('coy'))) return '1 Company';
          if (lower.includes('2') && (lower.includes('company') || lower.includes('coy'))) return '2 Company';
          if (lower.includes('3') && (lower.includes('company') || lower.includes('coy'))) return '3 Company';
          if (lower.includes('hq') && (lower.includes('company') || lower.includes('coy'))) return 'HQ company';
          return comp;
      };
      
      // Map username to company if company is not available (oc1, oc2, oc3, ochq)
      const mapUsernameToCompany = (uname) => {
          if (!uname) return null;
          const lower = uname.toLowerCase().trim();
          if (lower === 'oc1' || lower.includes('oc1')) return '1 Company';
          if (lower === 'oc2' || lower.includes('oc2')) return '2 Company';
          if (lower === 'oc3' || lower.includes('oc3')) return '3 Company';
          if (lower === 'ochq' || lower.includes('ochq') || lower === 'oc hq') return 'HQ company';
          return null;
      };
      
      let normalizedUserCompany = normalizeCompany(userCompany);
      
      // If company not found, try mapping from username
      if (!normalizedUserCompany && username) {
          normalizedUserCompany = mapUsernameToCompany(username);
      }
      
      // If user is OC (oc1, oc2, oc3, ochq), show only their company
      // Otherwise show all companies
      let companiesToShow = [];
      if (normalizedUserCompany && (normalizedUserCompany === '1 Company' || normalizedUserCompany === '2 Company' || normalizedUserCompany === '3 Company' || normalizedUserCompany === 'HQ company')) {
          // Show only the user's company
          companiesToShow = [normalizedUserCompany];
      } else {
          // Show all companies (for Admin, CO, etc.)
          companiesToShow = ['1 Company', '2 Company', '3 Company', 'HQ company'];
      }
      
      companiesToShow.forEach(companyName => {
          const option = document.createElement("option");
          option.value = companyName;
          option.textContent = companyName;
          companySelect.appendChild(option);
      });
      
      // Set default selection to user's company if available
      if (normalizedUserCompany && companiesToShow.includes(normalizedUserCompany)) {
          companySelect.value = normalizedUserCompany;
          // Trigger change event to load data for this company
          companySelect.dispatchEvent(new Event('change'));
      }
  } catch (err) {
      console.error("Error loading companies:", err);
  }
}

function getDeviationBadgeClass(deviationPercent) {
  if (deviationPercent === null || deviationPercent === undefined) return 'deviation-normal';
  const absDeviation = Math.abs(deviationPercent);
  if (absDeviation > 10) return 'deviation-overweight';
  if (absDeviation > 0) return 'deviation-underweight';
  return 'deviation-normal';
}

function formatDeviation(deviation) {
  if (deviation === null || deviation === undefined) return 'N/A';
  const sign = deviation > 0 ? '+' : '';
  return `${sign}${deviation}`;
}

async function fetchBarGraphData() {
  try {
      const jcoOrFilter = document.getElementById('jco-or-filter').value;
      const jcoSafeOrFilter = document.getElementById('jco-safe-or-filter').value;
      const url = currentCompany === "All" 
          ? `/weight_system/api/bar-graph-data?fitUnfitFilter=${jcoOrFilter}&safeCategoryFilter=${jcoSafeOrFilter}`
          : `/weight_system/api/bar-graph-data?company=${encodeURIComponent(currentCompany)}&fitUnfitFilter=${jcoOrFilter}&safeCategoryFilter=${jcoSafeOrFilter}`;
      
      const res = await fetch(url);
      if (!res.ok) throw new Error("Failed to fetch bar graph data");
      const data = await res.json();
      drawBarGraphs(data);
  } catch (err) {
      console.error("Error fetching bar graph data:", err);
      drawBarGraphs({
          fitUnfit: {
              labels: ['Fit', 'Unfit'],
              data: [110, 42]
          },
          safeCategory: {
              labels: ['shape', 'Category'],
              data: [34, 118]
          },
          jcoOrFit: {
              labels: ['JCO Fit', 'OR Fit'],
              data: [50, 60]
          },
          jcoSafeOrCategory: {
              labels: ['JCO Shape I', 'OR Category'],
              data: [34, 118]
          }
      });
  }
}



function drawBarGraphs(data) {
  console.group("📊 drawBarGraphs()");
  console.log("Incoming data:", data);

  try {
    if (window.fitUnfitChartInstance) {
      console.log("♻️ Destroying fitUnfitChart");
      window.fitUnfitChartInstance.destroy();
    }
    if (window.safeCategoryChartInstance) {
      console.log("♻️ Destroying safeCategoryChart");
      window.safeCategoryChartInstance.destroy();
    }
    if (window.jcoOrFitChartInstance) {
      console.log("♻️ Destroying jcoOrFitChart");
      window.jcoOrFitChartInstance.destroy();
    }
    if (window.jcoSafeOrCategoryChartInstance) {
      console.log("♻️ Destroying jcoSafeOrCategoryChart");
      window.jcoSafeOrCategoryChartInstance.destroy();
    }
  } catch (err) {
    console.error("❌ Error while destroying charts:", err);
  }

  const commonBarOptions = { /* unchanged */ };
  const commonDonutOptions = { /* unchanged */ };

  /* ================= FIT / UNFIT BAR ================= */
  console.group("📊 Fit / Unfit Bar Chart");
  console.log("Data:", data.fitUnfit);

  const fitUnfitCanvas = document.getElementById('fitUnfitChart');
  if (!fitUnfitCanvas) {
    console.error("❌ fitUnfitChart canvas NOT FOUND");
  } else {
    const fitUnfitCtx = fitUnfitCanvas.getContext('2d');
    window.fitUnfitChartInstance = new Chart(fitUnfitCtx, {
      type: 'bar',
      data: {
        labels: data.fitUnfit?.labels || ['Fit', 'Unfit'],
        datasets: [{
          label: 'Fit',
          data: data.fitUnfit?.data || [110, 42],
          backgroundColor: ['#38a169', '#e53e3e'],
          borderColor: ['#2f855a', '#c53030'],
          borderWidth: 1,
          borderRadius: 4,
          borderSkipped: false,
          barPercentage: 0.7
        }]
      },
      options: commonBarOptions
    });
    console.log("✅ Fit / Unfit Bar Chart Loaded");
  }
  console.groupEnd();

  /* ================= SAFE / CATEGORY BAR ================= */
  console.group("📊 Safe / Category Bar Chart");
  console.log("Data:", data.safeCategory);

  const safeCategoryCanvas = document.getElementById('safeCategoryChart');
  if (!safeCategoryCanvas) {
    console.error("❌ safeCategoryChart canvas NOT FOUND");
  } else {
    const safeCategoryCtx = safeCategoryCanvas.getContext('2d');
    window.safeCategoryChartInstance = new Chart(safeCategoryCtx, {
      type: 'bar',
      data: {
        labels: ['shape I', 'Category'],
        datasets: [{
          label: 'shape I',
          data: data.safeCategory?.data || [34, 118],
          backgroundColor: ['#3182ce', '#d69e2e'],
          borderColor: ['#2c5282', '#b7791f'],
          borderWidth: 1,
          borderRadius: 4,
          borderSkipped: false,
          barPercentage: 0.7
        }]
      },
      options: commonBarOptions
    });
    console.log("✅ Safe / Category Bar Chart Loaded");
  }
  console.groupEnd();

  /* ================= JCO / OR FIT DONUT ================= */
  console.group("🍩 JCO vs OR FIT Doughnut");
  console.log("Data:", data.jcoOrFit);

  const jcoOrFitCanvas = document.getElementById('jcoOrFitChart');
  if (!jcoOrFitCanvas) {
    console.error("❌ jcoOrFitChart canvas NOT FOUND");
  } else {
    const jcoOrFilter = document.getElementById('jco-or-filter').value;
    const jcoOrFitCtx = jcoOrFitCanvas.getContext('2d');
    window.jcoOrFitChartInstance = new Chart(jcoOrFitCtx, {
      type: 'doughnut',
      data: {
        labels: data.jcoOrFit?.labels || [
          `JCO ${jcoOrFilter}`,
          `OR ${jcoOrFilter}`
        ],
        datasets: [{
          label: `JCO vs OR ${jcoOrFilter}`,
          data: data.jcoOrFit?.data || [50, 60],
          backgroundColor: ['#2b6cb0', '#ed8936'],
          borderColor: ['#2c5282', '#dd6b20'],
          borderWidth: 1
        }]
      },
      options: commonDonutOptions
    });
    console.log("✅ JCO vs OR FIT Doughnut Loaded");
  }
  console.groupEnd();

  /* ================= JCO / OR SAFE / CATEGORY DONUT ================= */
  console.group("🍩 JCO vs OR SAFE/CATEGORY Doughnut");
  console.log("Data:", data.jcoSafeOrCategory);

  const jcoSafeCanvas = document.getElementById('jcoSafeOrCategoryChart');
  if (!jcoSafeCanvas) {
    console.error("❌ jcoSafeOrCategoryChart canvas NOT FOUND");
  } else {
    const jcoSafeOrFilter = document.getElementById('jco-safe-or-filter').value;
    const jcoSafeCtx = jcoSafeCanvas.getContext('2d');
    window.jcoSafeOrCategoryChartInstance = new Chart(jcoSafeCtx, {
      type: 'doughnut',
      data: {
        labels:  ['JCO', 'OR'],
        datasets: [{
          label: `JCO vs OR ${jcoSafeOrFilter}`,
          data: data.jcoSafeOrCategory?.data || [34, 118],
          backgroundColor: ['#3182ce', '#d69e2e'],
          borderColor: ['#2c5282', '#b7791f'],
          borderWidth: 1
        }]
      },
      options: commonDonutOptions
    });
    console.log("✅ JCO vs OR SAFE/CATEGORY Doughnut Loaded");
  }
  console.groupEnd();

  console.groupEnd(); // drawBarGraphs
}
function updateDoughnutCharts() {
  console.log("🔄 updateDoughnutCharts() called");

  const jcoOrFilter = document.getElementById('jco-or-filter').value;
  const jcoSafeOrFilter = document.getElementById('jco-safe-or-filter').value;

  console.log("📌 Selected Filters:", {
    jcoOrFilter,
    jcoSafeOrFilter,
    currentCompany
  });

  const url = currentCompany === "All" 
    ? `/weight_system/api/bar-graph-data?fitUnfitFilter=${jcoOrFilter}&safeCategoryFilter=${jcoSafeOrFilter}`
    : `/weight_system/api/bar-graph-data?company=${encodeURIComponent(currentCompany)}&fitUnfitFilter=${jcoOrFilter}&safeCategoryFilter=${jcoSafeOrFilter}`;

  console.log("🌐 Fetch URL:", url);

  fetch(url)
    .then(res => {
      console.log("📡 Fetch response status:", res.status);
      if (!res.ok) throw new Error("Failed to fetch bar graph data");
      return res.json();
    })
    .then(data => {
      console.log("✅ API Response Data:", data);

      if (window.jcoOrFitChartInstance) {
        console.log("🧹 Destroying existing JCO vs OR chart");
        window.jcoOrFitChartInstance.destroy();
      }

      if (window.jcoSafeOrCategoryChartInstance) {
        console.log("🧹 Destroying existing JCO Safe/Category chart");
        window.jcoSafeOrCategoryChartInstance.destroy();
      }

      const commonDonutOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: { color: '#4a5568', font: { size: 12 } }
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                return `${context.label}: ${context.parsed}`;
              }
            }
          }
        },
        animation: { duration: 1000, easing: 'easeOutQuart' }
      };

      console.log("🍩 Creating JCO vs OR Doughnut Chart");
      console.log("📊 jcoOrFit data:", data.jcoOrFit);

      const jcoOrFitCtx = document.getElementById('jcoOrFitChart').getContext('2d');
      window.jcoOrFitChartInstance = new Chart(jcoOrFitCtx, {
        type: 'doughnut',
        data: {
          labels: [
            `JCO ${jcoOrFilter.charAt(0).toUpperCase() + jcoOrFilter.slice(1)}`,
            `OR ${jcoOrFilter.charAt(0).toUpperCase() + jcoOrFilter.slice(1)}`
          ],
          datasets: [{
            label: `JCO vs OR ${jcoOrFilter}`,
            data: data.jcoOrFit?.data || [50, 60],
            backgroundColor: ['#2b6cb0', '#ed8936'],
            borderColor: ['#2c5282', '#dd6b20'],
            borderWidth: 1
          }]
        },
        options: commonDonutOptions
      });

      console.log("🍩 Creating JCO Safe/Category Doughnut Chart");
      console.log("📊 jcoSafeOrCategory data:", data.jcoSafeOrCategory);

      const jcoSafeOrCategoryCtx = document.getElementById('jcoSafeOrCategoryChart').getContext('2d');
      window.jcoSafeOrCategoryChartInstance = new Chart(jcoSafeOrCategoryCtx, {
        type: 'doughnut',
        data: {
          labels: data.jcoSafeOrCategory?.labels || [
            `JCO ${jcoSafeOrFilter.charAt(0).toUpperCase()}`,
            `OR ${jcoSafeOrFilter.charAt(0).toUpperCase()}`
          ],
          datasets: [{
            label: `JCO vs OR ${jcoSafeOrFilter}`,
            data: data.jcoSafeOrCategory?.data || [34, 118],
            backgroundColor: [
              "#3182ce",
              "#2c5282",
              "#d69e2e",
              "#b7791f"
            ],
            borderColor: ['#2c5282', '#b7791f'],
            borderWidth: 1
          }]
        },
        options: {
          ...commonDonutOptions,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                boxWidth: 15,
                font: { size: 12 }
              }
            }
          }
        }
      });

      console.log("✅ Doughnut charts updated successfully");
    })
    .catch(err => {
      console.error("❌ Error updating doughnut charts:", err);
      showValidationPopup("Failed to update chart data. Please try again.");
    });
}

function resetChartVisibility() {
  document.getElementById("bar-charts-container").style.display = "block";
}

async function fetchSummary(company = "All") {
  showLoader("fullscreen-loader", true);
  currentCompany = company;
  
  if (company === "All") {
      document.getElementById("company-badge").textContent = "15 CESR";
  } else {
      const companyNumber = company.match(/\d+/);
      document.getElementById("company-badge").textContent = companyNumber ? `${companyNumber[0]} Company` : company;
  }

  try {
      const summaryUrl = company === "All" ? "/weight_system/api/summary" : `/weight_system/api/summary?company=${encodeURIComponent(company)}`;
      const statusUrl = company === "All" ? "/weight_system/api/status-summary" : `/weight_system/api/status-summary?company=${encodeURIComponent(company)}`;

      const [summaryRes, statusRes] = await Promise.all([
          fetch(summaryUrl).then(res => {
              if (!res.ok) throw new Error("Failed to fetch summary");
              return res.json();
          }),
          fetch(statusUrl).then(res => {
              if (!res.ok) throw new Error("Failed to fetch status summary");
              return res.json();
          }),
          fetchBarGraphData() // Ensure bar graph data is fetched
      ]);

      document.getElementById("total-count").textContent = summaryRes.total ?? 0;
      document.getElementById("unauth-count").textContent = summaryRes.unFit ?? 0;
      document.getElementById("auth-count").textContent = summaryRes.Fit ?? 0;
      document.getElementById("safe-count").textContent = statusRes.safe_count ?? 0;
      document.getElementById("category-count").textContent = statusRes.category_count ?? 0;

      unFitCount = summaryRes.unFit ?? 0;
      fitCount = summaryRes.Fit ?? 0;
      safeCount = statusRes.safe_count ?? 0;
      categoryCount = statusRes.category_count ?? 0;

      resetChartVisibility();
  } catch (err) {
      console.error("Error fetching summary:", err);
      document.getElementById("total-count").textContent = "0";
      document.getElementById("unauth-count").textContent = "0";
      document.getElementById("auth-count").textContent = "0";
      document.getElementById("safe-count").textContent = "0";
      document.getElementById("category-count").textContent = "0";
      fetchBarGraphData();
  } finally {
      showLoader("fullscreen-loader", false);
  }
}

function filterTableByDeviation(rows, deviationRange) {
  if (deviationRange === "all") return rows;
  
  return rows.filter(row => {
      const deviationPercent = row.weight_deviation_percent;
      if (deviationPercent === null || deviationPercent === undefined) return false;
      
      const absDeviation = Math.abs(deviationPercent);
      switch (deviationRange) {
          case "0-10":
              return absDeviation > 0 && absDeviation <= 10;
          case "10-20":
              return absDeviation > 10 && absDeviation <= 20;
          case "more-than-20":
              return absDeviation > 20;
          default:
              return true;
      }
  });
}

function filterTableByRank(rows, rankFilter) {
  if (rankFilter === "all") return rows;
  
  return rows.filter(row => {
      if (rankFilter === "JCO") {
          return row.rank === "JCO";
      } else if (rankFilter === "other") {
          return row.rank !== "JCO";
      }
      
      return true;
  });
}

function renderTableRows(rows, statusClass, append = false) {
  const tbody = document.getElementById("table-wrapper").querySelector("tbody");
  if (!append) {
      tbody.innerHTML = "";
  }

  if (!rows.length && !append) {
      tbody.innerHTML = '<tr><td colspan="13" style="text-align: center; color: #718096; padding: 2rem;">No records found</td></tr>';
      return;
  }

  rows.forEach(r => {
      console.log(r,"this is r")
      const ideal = r.ideal_weight ? r.ideal_weight.toFixed(2) : "—";
      const lower = r.lower_limit ? r.lower_limit.toFixed(2) : "—";
      const upper = r.upper_limit ? r.upper_limit.toFixed(2) : "—";
      const deviationPercent = r.weight_deviation_percent;
      const deviationKg = r.weight_deviation_kg;
      const deviationBadgeClass = getDeviationBadgeClass(deviationPercent);
      const deviationPercentText = formatDeviation(deviationPercent);
      const deviationKgText = formatDeviation(deviationKg);
      
      // For status rows, use the actual status_type from the row data
      // For fit/unfit rows, use the statusClass parameter
      let buttonStatusClass = statusClass;
      if (statusClass === "status" && r.status_type) {
          buttonStatusClass = r.status_type; // Use "shape" or "category" instead of "status"
      }
      
      const tr = document.createElement("tr");
      tr.innerHTML = `
          <td>${r.army_number}</td>
          <td>${r.name}</td>
          <td>${r.rank}</td>
          <td>${r.company}</td>
          <td>${r.age}</td>
          <td>${r.height_cm}</td>
          <td>${lower} - ${upper}</td>
          <td>${r.actual_weight}</td>
          <td><span class="deviation-badge ${deviationBadgeClass}">${deviationKgText} kg</span></td>
          <td><span class="deviation-badge ${deviationBadgeClass}">${deviationPercentText}%</span></td>
          <td><span class="status-badge ${statusClass}">${r.status.toUpperCase()}</span></td>
          <td><span class="status-type-badge">${r.status_type.toUpperCase()}</span></td>
          <td><button type="button" class="view-person-btn" data-army-number="${r.army_number}" data-status-class="${buttonStatusClass}" data-status="${r.status || ''}">View</button></td>
      `;
      tbody.appendChild(tr);
      
      // Add click handler: use row data we already have (no API needed)
      const viewBtn = tr.querySelector('.view-person-btn');
      if (viewBtn) {
        const rowData = { ...r };
        const btnStatusClass = buttonStatusClass;
        viewBtn.addEventListener('click', function(e) {
          e.preventDefault();
          e.stopPropagation();
          showPersonModalWithData(rowData, btnStatusClass);
        });
      }
  });
}

/**
 * Show person details modal using data we already have (from table row).
 * No API call - displays immediately with actual row data.
 */
function showPersonModalWithData(data, statusClass) {
  const modal = document.getElementById('person-details-modal');
  const body = document.getElementById('person-details-body');
  if (!modal || !body) {
    console.error('Modal elements not found');
    alert('Could not open details. Please refresh the page.');
    return;
  }
  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';
  const normalized = normalizePersonData(data);
  renderPersonDetails(normalized, statusClass);
}
window.showPersonModalWithData = showPersonModalWithData;

/**
 * Ensure person data has proper types for display (numbers where needed).
 */
function normalizePersonData(data) {
  const num = (v) => (v === null || v === undefined) ? null : Number(v);
  return {
    army_number: data.army_number,
    name: data.name,
    rank: data.rank,
    company: data.company,
    age: num(data.age) ?? data.age,
    height_cm: num(data.height_cm) ?? data.height_cm,
    actual_weight: num(data.actual_weight) ?? data.actual_weight,
    status_type: data.status_type,
    category_type: data.category_type,
    restrictions: data.restrictions,
    ideal_weight: num(data.ideal_weight) ?? data.ideal_weight,
    lower_limit: num(data.lower_limit) ?? data.lower_limit,
    upper_limit: num(data.upper_limit) ?? data.upper_limit,
    status: data.status,
    weight_deviation_percent: num(data.weight_deviation_percent) ?? data.weight_deviation_percent,
    weight_deviation_kg: num(data.weight_deviation_kg) ?? data.weight_deviation_kg
  };
}

async function fetchAndShow(url, statusClass) {
  const wrapper = document.getElementById("table-wrapper");
  const tbody = wrapper.querySelector("tbody");
  const barChartsContainer = document.getElementById("bar-charts-container");
  const closeButton = document.getElementById("close-table-btn");
  const deviationFilter = document.getElementById("deviation-filter");
  const rankFilter = document.getElementById("rank-filter");

  barChartsContainer.style.display = "none";
  closeButton.style.display = "block";
  deviationFilter.style.display = statusClass === "unauth" ? "block" : "none";
  rankFilter.style.display = "block";

  tbody.innerHTML = "";
  tableData = [];
  displayedData = [];
  currentPage = 1;
  hasMoreData = true;

  wrapper.style.display = "block";
  showLoader("table-spinner", true);
  isLoading = true;

  try {
      let finalUrl = currentCompany === "All" 
          ? url
          : `${url}?company=${encodeURIComponent(currentCompany)}`;
      const res = await fetch(finalUrl);
      if (!res.ok) throw new Error("Failed to fetch table data");
      const data = await res.json();
      
      tableData = data.rows || [];
      currentStatusClass = statusClass;

      if (tableData.length === 0) {
          tbody.innerHTML = '<tr><td colspan="13" style="text-align: center; color: #718096; padding: 2rem;">No records found</td></tr>';
          hasMoreData = false;
          return;
      }

      let filteredRows = tableData.slice(0, rowsPerPage);
      if (statusClass === "unauth") {
          filteredRows = filterTableByDeviation(filteredRows, deviationFilter.value);
      }
      filteredRows = filterTableByRank(filteredRows, rankFilter.value);
      
      displayedData = filteredRows;
      renderTableRows(filteredRows, statusClass);
      hasMoreData = tableData.length > rowsPerPage;
  } catch (err) {
      console.error("Error fetching table data:", err);
      tbody.innerHTML = '<tr><td colspan="13" style="text-align: center; color: #718096; padding: 2rem;">Error loading data</td></tr>';
      hasMoreData = false;
  } finally {
      showLoader("table-spinner", false);
      isLoading = false;
  }
}

async function fetchStatusData(statusType) {
  const wrapper = document.getElementById("table-wrapper");
  const tbody = wrapper.querySelector("tbody");
  const barChartsContainer = document.getElementById("bar-charts-container");
  const closeButton = document.getElementById("close-table-btn");
  const deviationFilter = document.getElementById("deviation-filter");
  const rankFilter = document.getElementById("rank-filter");

  barChartsContainer.style.display = "none";
  closeButton.style.display = "block";
  deviationFilter.style.display = "none";
  rankFilter.style.display = "block";

  tbody.innerHTML = "";
  tableData = [];
  displayedData = [];
  currentPage = 1;
  hasMoreData = true;

  wrapper.style.display = "block";
  showLoader("table-spinner", true);
  isLoading = true;

  try {
      let finalUrl = currentCompany === "All" 
          ? `/weight_system/api/status-data?status_type=${statusType}`
          : `/weight_system/api/status-data?status_type=${statusType}&company=${encodeURIComponent(currentCompany)}`;
      
      const res = await fetch(finalUrl);
      if (!res.ok) throw new Error("Failed to fetch status data");
      const data = await res.json();
      
      tableData = data.rows || [];
      currentStatusClass = "status";

      if (tableData.length === 0) {
          tbody.innerHTML = '<tr><td colspan="13" style="text-align: center; color: #718096; padding: 2rem;">No records found</td></tr>';
          hasMoreData = false;
          return;
      }

      const filteredRows = filterTableByRank(tableData.slice(0, rowsPerPage), rankFilter.value);
      
      displayedData = filteredRows;
      renderTableRows(filteredRows, "status");
      hasMoreData = tableData.length > rowsPerPage;
  } catch (err) {
      console.error("Error fetching status data:", err);
      tbody.innerHTML = '<tr><td colspan="13" style="text-align: center; color: #718096; padding: 2rem;">Error loading data</td></tr>';
      hasMoreData = false;
  } finally {
      showLoader("table-spinner", false);
      isLoading = false;
  }
}

function loadMoreRows() {
  if (!hasMoreData || isLoading) return;

  isLoading = true;
  const deviationFilter = document.getElementById("deviation-filter");
  const rankFilter = document.getElementById("rank-filter");
  const statusClass = currentStatusClass;

  const startIndex = currentPage * rowsPerPage;
  const endIndex = startIndex + rowsPerPage;
  let nextRows = tableData.slice(startIndex, endIndex);

  if (statusClass === "unauth") {
      nextRows = filterTableByDeviation(nextRows, deviationFilter.value);
  }
  nextRows = filterTableByRank(nextRows, rankFilter.value);

  if (nextRows.length === 0) {
      hasMoreData = false;
      isLoading = false;
      return;
  }

  displayedData = [...displayedData, ...nextRows];
  renderTableRows(nextRows, statusClass, true);
  currentPage++;
  hasMoreData = endIndex < tableData.length;
  isLoading = false;
}

function closeTable() {
  const wrapper = document.getElementById("table-wrapper");
  const closeButton = document.getElementById("close-table-btn");
  const deviationFilter = document.getElementById("deviation-filter");
  const rankFilter = document.getElementById("rank-filter");

  wrapper.style.display = "none";
  closeButton.style.display = "none";
  deviationFilter.style.display = "none";
  rankFilter.style.display = "none";
  wrapper.querySelector("tbody").innerHTML = "";
  tableData = [];
  displayedData = [];
  currentPage = 1;
  hasMoreData = true;
  resetChartVisibility();
}

function handleScroll() {
  const tableWrapper = document.getElementById("table-wrapper");
  if (tableWrapper.style.display === "none") return;

  const scrollTop = tableWrapper.scrollTop;
  const scrollHeight = tableWrapper.scrollHeight;
  const clientHeight = tableWrapper.clientHeight;

  if (scrollTop + clientHeight >= scrollHeight - 50 && !isLoading && hasMoreData) {
      loadMoreRows();
  }
}

document.getElementById("load-unauth-btn").addEventListener("click", () => fetchAndShow("/weight_system/api/unauthorized", "unauth"));
document.getElementById("load-auth-btn").addEventListener("click", () => fetchAndShow("/weight_system/api/authorized", "auth"));
document.getElementById("load-safe-btn").addEventListener("click", () => fetchStatusData("shape"));
document.getElementById("load-category-btn").addEventListener("click", () => fetchStatusData("category"));
document.getElementById("close-table-btn").addEventListener("click", closeTable);
document.getElementById("table-wrapper").addEventListener("scroll", handleScroll);

document.getElementById("company-select").addEventListener("change", (e) => {
  fetchSummary(e.target.value);
  closeTable();
});

document.getElementById("deviation-filter").addEventListener("change", (e) => {
  if (currentStatusClass === "unauth") {
      showLoader("table-spinner", true);
      setTimeout(() => {
          let filteredRows = filterTableByDeviation(tableData.slice(0, currentPage * rowsPerPage), e.target.value);
          filteredRows = filterTableByRank(filteredRows, document.getElementById("rank-filter").value);
          displayedData = filteredRows;
          renderTableRows(filteredRows, currentStatusClass);
          hasMoreData = tableData.length > currentPage * rowsPerPage;
          showLoader("table-spinner", false);
      }, 300);
  }
});

document.getElementById("rank-filter").addEventListener("change", (e) => {
  showLoader("table-spinner", true);
  setTimeout(() => {
      let filteredRows = tableData.slice(0, currentPage * rowsPerPage);
      if (currentStatusClass === "unauth") {
          filteredRows = filterTableByDeviation(filteredRows, document.getElementById("deviation-filter").value);
      }
      filteredRows = filterTableByRank(filteredRows, e.target.value);
      displayedData = filteredRows;
      renderTableRows(filteredRows, currentStatusClass);
      hasMoreData = tableData.length > currentPage * rowsPerPage;
      showLoader("table-spinner", false);
  }, 300);
});

document.addEventListener('DOMContentLoaded', function() {
  const deviationFilter = document.getElementById('deviation-filter');
  deviationFilter.innerHTML = `
      <option value="all">All Deviations</option>
      <option value="0-10">0% to 10%</option>
      <option value="10-20">10% to 20%</option>
      <option value="more-than-20">More than 20%</option>
  `;
  
  const rankFilter = document.getElementById('rank-filter');
  rankFilter.innerHTML = `
      <option value="all">All Ranks</option>
      <option value="JCO">JCO</option>
      <option value="other">Other than JCO</option>
  `;

  // Toggle category fields for Add User modal
  const addStatusRadios = document.getElementsByName('status_type');
  const addCategoryOptions = document.getElementById('category-options');
  const addRestrictionsGroup = document.getElementById('restrictions-group');

  addStatusRadios.forEach(radio => {
      radio.addEventListener('change', () => {
          if (radio.value === 'category') {
              addCategoryOptions.style.display = 'flex';
              addRestrictionsGroup.style.display = 'block';
          } else {
              addCategoryOptions.style.display = 'none';
              addRestrictionsGroup.style.display = 'none';
              document.querySelectorAll('input[name="category_type"]').forEach(r => r.checked = false);
              document.getElementById('restrictions').value = '';
          }
      });
  });

  // Toggle category fields for Update User modal
  const editStatusRadios = document.getElementsByName('edit-status_type');
  const editCategoryOptions = document.getElementById('edit-category-options');
  const editRestrictionsGroup = document.getElementById('edit-restrictions-group');

  editStatusRadios.forEach(radio => {
      radio.addEventListener('change', () => {
          if (radio.value === 'category') {
              editCategoryOptions.style.display = 'flex';
              editRestrictionsGroup.style.display = 'block';
          } else {
              editCategoryOptions.style.display = 'none';
              editRestrictionsGroup.style.display = 'none';
              document.querySelectorAll('input[name="edit-category_type"]').forEach(r => r.checked = false);
              document.getElementById('edit-restrictions').value = '';
          }
      });
  });

  document.getElementById('jco-or-filter').addEventListener('change', updateDoughnutCharts);
  document.getElementById('jco-safe-or-filter').addEventListener('change', updateDoughnutCharts);

  showLoader("fullscreen-loader", true);
  Promise.all([
      loadCompanies(),
      fetchSummary()
  ]).finally(() => {
      // Fullscreen loader is hidden in fetchSummary after all data is loaded
  });
});

function validateAlpha(input) {
  console.log('within validate aplha')
  const value = input.value;
  const errorElement = document.getElementById(input.id + '-error');
  const regex = /^[a-zA-Z\s]*$/;
  
  if (!regex.test(value)) {
      errorElement.textContent = 'Only letters and spaces are allowed';
      input.style.borderColor = '#e53e3e';
      return false;
  } else {
      errorElement.textContent = '';
      input.style.borderColor = '';
      return true;
  }
}

function validateAlphaNumeric(input) {
  console.log("within alpha Numeric")
  const value = input.value;
  const errorElement = document.getElementById(input.id + '-error');
  const regex = /^[a-zA-Z0-9]*$/;
  
  if (!regex.test(value)) {
      errorElement.textContent = 'Only letters and numbers are allowed';
      input.style.borderColor = '#e53e3e';
      return false;
  } else {
      errorElement.textContent = '';
      input.style.borderColor = '';
      return true;
  }
}

function validateNumeric(input) {
  const value = input.value;
  const errorElement = document.getElementById(input.id + '-error');
  const regex = /^[0-9.]*$/;
  
  if (!regex.test(value)) {
      errorElement.textContent = 'Only numbers are allowed';
      input.style.borderColor = '#e53e3e';
      return false;
  } else if (value && (isNaN(parseFloat(value)) || !isFinite(value))) {
      errorElement.textContent = 'Please enter a valid number';
      input.style.borderColor = '#e53e3e';
      return false;
  } else {
      errorElement.textContent = '';
      input.style.borderColor = '';
      return true;
  }
}

function validateRestrictions(input) {
  const value = input.value;
  const errorElement = document.getElementById(input.id + '-error');
  
  if (value.length > 500) {
      errorElement.textContent = 'Restrictions cannot exceed 500 characters';
      input.style.borderColor = '#e53e3e';
      return false;
  } else {
      errorElement.textContent = '';
      input.style.borderColor = '';
      return true;
  }
}

function openAddUserModal() {
  const modal = document.getElementById('add-user-modal');
  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';
  document.getElementById('add-user-form').reset();
  document.querySelectorAll('#add-user-form .error-message').forEach(el => el.textContent = '');
  document.querySelectorAll('#add-user-form .form-group input, #add-user-form .form-group select, #add-user-form .form-group textarea').forEach(el => el.style.borderColor = '');
  document.getElementById('category-options').style.display = 'none';
  document.getElementById('restrictions-group').style.display = 'none';
  document.querySelector('input[name="status_type"][value="safe"]').checked = true;
}

function closeAddUserModal() {
  const modal = document.getElementById('add-user-modal');
  modal.style.display = 'none';
  document.body.style.overflow = 'auto';
}

function showSuccessToast(message) {
  console.log(message,"this is msg")
  const toast = document.getElementById('success-toast');
  const toastMessage = document.getElementById('message-text');
  toast.textContent = message
  console.log(toastMessage.textContent)
  toast.style.display = 'block';
  
  setTimeout(() => {
      toast.style.display = 'none';
  }, 3000);
}

async function handleAddUserSubmit(event) {
  event.preventDefault();
  
  const ageInput = document.getElementById('age');
  const ageValue = parseInt(ageInput.value);
  if (ageValue < 18) {
      showValidationPopup('Age should not be less than 18 years');
      return;
  }
  
  const heightInput = document.getElementById('height_cm');
  const heightValue = parseInt(heightInput.value);
  if (heightValue < 156) {
      showValidationPopup('Height should not be less than 156 cm');
      return;
  }
  
  const fields = [
      { id: 'name', validator: validateAlpha },
      { id: 'army_number', validator: validateAlphaNumeric },
      { id: 'age', validator: validateNumeric },
      { id: 'rank', validator: validateAlpha },
      { id: 'height_cm', validator: validateNumeric },
      { id: 'actual_weight', validator: validateNumeric }
  ];
  
  let isValid = true;
  
  fields.forEach(field => {
      const input = document.getElementById(field.id);
      if (!field.validator(input)) {
          isValid = false;
      }
  });
  
  const companySelect = document.getElementById('company');
  const companyError = document.getElementById('company-error');
  if (!companySelect.value) {
      companyError.textContent = 'Please select a company';
      companySelect.style.borderColor = '#e53e3e';
      isValid = false;
  } else {
      companyError.textContent = '';
      companySelect.style.borderColor = '';
  }

  const statusType = document.querySelector('input[name="status_type"]:checked').value;
  let categoryType = null;
  let restrictions = null;
  
  if (statusType === 'category') {
      const categoryRadios = document.getElementsByName('category_type');
      const isCategorySelected = Array.from(categoryRadios).some(radio => radio.checked);
      const restrictionsInput = document.getElementById('restrictions');
      const restrictionsError = document.getElementById('restrictions-error');

      if (!isCategorySelected) {
          restrictionsError.textContent = 'Please select a category type';
          isValid = false;
      } else {
          categoryType = document.querySelector('input[name="category_type"]:checked').value;
          if (!validateRestrictions(restrictionsInput)) {
              isValid = false;
          } else {
              restrictions = restrictionsInput.value.trim();
          }
      }
  }
  
  if (!isValid) {
      return;
  }
  
  const formData = {
      name: document.getElementById('name').value.trim(),
      army_number: document.getElementById('army_number').value.trim(),
      rank: document.getElementById('rank').value.trim(),
      age: parseInt(document.getElementById('age').value),
      height_cm: parseInt(document.getElementById('height_cm').value),
      actual_weight: parseFloat(document.getElementById('actual_weight').value),
      company: document.getElementById('company').value,
      status_type: statusType,
      category_type: categoryType,
      restrictions: restrictions
  };
  
  try {
      const response = await fetch('/weight_system/api/add-user', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
      });
      
      const result = await response.json();
      
      if (response.ok) {
          showSuccessToast('User added Successfully..');
          closeAddUserModal();
          setTimeout(() => {
              fetchSummary(currentCompany);
          }, 1500);
      } else {
          if (result.error && result.error.includes('army number')) {
              document.getElementById('army_number-error').textContent = result.error;
              document.getElementById('army_number').style.borderColor = '#e53e3e';
          } else {
              showValidationPopup('Error adding user: ' + (result.error || 'Unknown error'));
          }
      }
  } catch (error) {
      console.error('Error adding user:', error);
      showValidationPopup('Error adding user. Please try again.');
  }
}

// Update User Modal Functions
function openUpdateUserModal() {
  const modal = document.getElementById('update-user-modal');
  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';
  document.getElementById('update-user-form').style.display = 'block';
  document.getElementById('edit-user-form').style.display = 'none';
  document.getElementById('update-army-number').value = '';
}

document.getElementsByClassName('button-update-cancel')[0].addEventListener('click',function(){
  closeUpdateUserModal()
})

function closeUpdateUserModal() {
  const modal = document.getElementById('update-user-modal');
  console.log("Update close model is called.....")
  modal.style.display = 'none';
  document.body.style.overflow = 'auto';
  resetEditForm();
}

function resetEditForm() {
  document.getElementById('edit-user-form').reset();
  document.querySelectorAll('#edit-user-form .error-message').forEach(el => {
      el.textContent = '';
  });
  document.querySelectorAll('#edit-user-form .form-group input, #edit-user-form .form-group select, #edit-user-form .form-group textarea').forEach(el => {
      el.style.borderColor = '';
  });
  document.getElementById('edit-category-options').style.display = 'none';
  document.getElementById('edit-restrictions-group').style.display = 'none';
  document.querySelector('input[name="edit-status_type"][value="safe"]').checked = true;
}

async function handleUpdateUserSearch(event) {
  event.preventDefault();
  const armyNumber = document.getElementById('update-army-number').value.trim();
  if (!armyNumber) {
      showValidationPopup('Please enter an Army Number.');
      return;
  }

  showLoader('validation-popup', true); // Reuse loader for feedback
  try {
      const response = await fetch(`/weight_system/api/user/${encodeURIComponent(armyNumber)}`);
      
       
      const user = await response.json();
      if(user.error){
        alert(user.error)
        return
      }

      document.getElementById('update-user-form').style.display = 'none';
      document.getElementById('edit-user-form').style.display = 'block';
      document.getElementById('edit-name').value = user.name;
      document.getElementById('edit-army_number').value = user.army_number;
      document.getElementById('edit-age').value = user.age;
      document.getElementById('edit-rank').value = user.rank;
      document.getElementById('edit-height_cm').value = user.height_cm;
      document.getElementById('edit-actual_weight').value = user.actual_weight;
      document.getElementById('edit-company').value = user.company;
      document.querySelector(`input[name="edit-status_type"][value="${user.status_type}"]`).checked = true;
      if (user.category_type) {
          document.getElementById('edit-category-options').style.display = 'flex';
          document.querySelector(`input[name="edit-category_type"][value="${user.category_type}"]`).checked = true;
          document.getElementById('edit-restrictions-group').style.display = 'block';
      } else {
          document.getElementById('edit-category-options').style.display = 'none';
          document.getElementById('edit-restrictions-group').style.display = 'none';
      }
      document.getElementById('edit-restrictions').value = user.restrictions || '';
  } catch (error) {
      console.error('Error fetching user:', error);
      showValidationPopup('User not found or error occurred. Please try again.');
  } finally {
      showLoader('validation-popup', false);
  }
}

async function handleUpdateUserSubmit(event) {
  event.preventDefault();

  const fields = [
      { id: 'edit-name', validator: validateAlpha },
      { id: 'edit-army_number', validator: validateAlphaNumeric, readonly: true },
      { id: 'edit-age', validator: validateNumeric },
      { id: 'edit-rank', validator: validateAlpha },
      { id: 'edit-height_cm', validator: validateNumeric },
      { id: 'edit-actual_weight', validator: validateNumeric }
  ];

  let isValid = true;
  fields.forEach(field => {
      const input = document.getElementById(field.id);
      if (!field.readonly && !field.validator(input)) {
          isValid = false;
      }
  });

  const companySelect = document.getElementById('edit-company');
  const companyError = document.getElementById('edit-company-error');
  if (!companySelect.value) {
      companyError.textContent = 'Please select a company';
      companySelect.style.borderColor = '#e53e3e';
      isValid = false;
  } else {
      companyError.textContent = '';
      companySelect.style.borderColor = '';
  }

  const statusType = document.querySelector('input[name="edit-status_type"]:checked').value;
  let categoryType = null;
  let restrictions = null;

  if (statusType === 'category') {
      const categoryRadios = document.getElementsByName('edit-category_type');
      const isCategorySelected = Array.from(categoryRadios).some(radio => radio.checked);
      const restrictionsInput = document.getElementById('edit-restrictions');
      const restrictionsError = document.getElementById('edit-restrictions-error');

      if (!isCategorySelected) {
          restrictionsError.textContent = 'Please select a category type';
          isValid = false;
      } else {
          categoryType = document.querySelector('input[name="edit-category_type"]:checked').value;
          if (!validateRestrictions(restrictionsInput)) {
              isValid = false;
          } else {
              restrictions = restrictionsInput.value.trim();
          }
      }
  }

  if (!isValid) {
      return;
  }

  const formData = {
      army_number: document.getElementById('edit-army_number').value.trim(),
      name: document.getElementById('edit-name').value.trim(),
      rank: document.getElementById('edit-rank').value.trim(),
      age: parseInt(document.getElementById('edit-age').value),
      height_cm: parseInt(document.getElementById('edit-height_cm').value),
      actual_weight: parseFloat(document.getElementById('edit-actual_weight').value),
      company: document.getElementById('edit-company').value,
      status_type: statusType,
      category_type: categoryType,
      restrictions: restrictions
  };

  try {
      const response = await fetch('/weight_system/api/update-user', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
      });

      const result = await response.json();
      if (response.ok) {
          showSuccessToast('User updated Successfully..');
          closeUpdateUserModal();
          setTimeout(() => {
              fetchSummary(currentCompany);
          }, 1500);
      } else {
          showValidationPopup('Error updating user: ' + (result.error || 'Unknown error'));
      }
  } catch (error) {
      console.error('Error updating user:', error);
      showValidationPopup('Error updating user. Please try again.');
  }
}

// Event Listeners
document.getElementById('add-user-btn').addEventListener('click', openAddUserModal);
document.querySelector('#add-user-modal .close-modal').addEventListener('click', closeAddUserModal);
document.getElementById('add-user-form').addEventListener('submit', handleAddUserSubmit);
document.getElementById('add-user-modal').addEventListener('click', function(event) {
  if (event.target === this) {
      closeAddUserModal();
  }
});

document.getElementById('update-user-btn').addEventListener('click', openUpdateUserModal);
document.querySelector('#update-user-modal .close-modal').addEventListener('click', closeUpdateUserModal);
document.getElementById('update-user-form').addEventListener('submit', handleUpdateUserSearch);
document.getElementById('edit-user-form').addEventListener('submit', handleUpdateUserSubmit);
document.getElementById('update-user-modal').addEventListener('click', function(event) {
  if (event.target === this) {
      closeUpdateUserModal();
  }
});

// Person Details Modal Functions - Make globally accessible
window.viewPersonDetails = async function(armyNumber, statusClass) {
  console.log('🔍 viewPersonDetails called with:', { armyNumber, statusClass });
  
  if (!armyNumber || !statusClass) {
    console.error('❌ Missing required parameters:', { armyNumber, statusClass });
    alert('Error: Missing person information. Please try again.');
    return;
  }
  
  const modal = document.getElementById('person-details-modal');
  const body = document.getElementById('person-details-body');
  
  if (!modal) {
    console.error('❌ Modal element not found!');
    alert('Modal element not found. Please refresh the page.');
    return;
  }
  
  if (!body) {
    console.error('❌ Modal body element not found!');
    return;
  }
  
  // Show modal
  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';
  
  // Show loading state
  body.innerHTML = `
    <div style="text-align: center; padding: 40px;">
      <div class="spinner" style="margin: 0 auto;"></div>
      <p style="margin-top: 15px; color: var(--text-secondary); font-size: 1rem;">Loading person details...</p>
    </div>
  `;
  
  try {
    const url = `/weight_system/api/person-details/${encodeURIComponent(armyNumber)}?status_class=${encodeURIComponent(statusClass)}`;
    console.log('🌐 Fetching from URL:', url);
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    
    console.log('📡 Response status:', response.status);
    
    if (!response.ok) {
      let errorText = 'Unknown error';
      try {
        const errorData = await response.json();
        errorText = errorData.error || errorData.message || `HTTP ${response.status}`;
      } catch (e) {
        errorText = await response.text() || `HTTP ${response.status}`;
      }
      console.error('❌ Response not OK:', response.status, errorText);
      throw new Error(errorText);
    }
    
    const data = await response.json();
    console.log('✅ Received data:', data);
    
    if (data.error) {
      body.innerHTML = `
        <div style="text-align: center; padding: 40px; color: var(--danger-color);">
          <i class="fas fa-exclamation-circle" style="font-size: 3rem; margin-bottom: 15px;"></i>
          <p style="font-size: 1.1rem; font-weight: 600;">${data.error}</p>
        </div>
      `;
      return;
    }
    
    // Render the details
    renderPersonDetails(data, statusClass);
    console.log('✅ Person details rendered successfully');
    
  } catch (error) {
    console.error('❌ Error fetching person details:', error);
    body.innerHTML = `
      <div style="text-align: center; padding: 40px; color: var(--danger-color);">
        <i class="fas fa-exclamation-triangle" style="font-size: 3rem; margin-bottom: 15px;"></i>
        <p style="font-size: 1.1rem; font-weight: 600; margin-bottom: 10px;">Error loading person details</p>
        <p style="font-size: 0.9rem; color: var(--text-secondary);">${error.message || 'Please try again later.'}</p>
        <button onclick="window.closePersonDetailsModal()" style="margin-top: 20px; padding: 10px 20px; background: var(--primary-color); color: white; border: none; border-radius: 8px; cursor: pointer;">Close</button>
      </div>
    `;
  }
}

// Make sure function is available immediately
console.log('✅ viewPersonDetails function registered:', typeof window.viewPersonDetails);

function renderPersonDetails(data, statusClass) {
  const body = document.getElementById('person-details-body');
  if (!body) return;

  const toNum = (v) => (v !== null && v !== undefined && !isNaN(Number(v))) ? Number(v) : null;
  const idealWeight = toNum(data.ideal_weight);
  const lowerLimit = toNum(data.lower_limit);
  const upperLimit = toNum(data.upper_limit);
  const actualWeight = toNum(data.actual_weight);
  const ideal = idealWeight != null ? idealWeight.toFixed(2) : "—";
  const lower = lowerLimit != null ? lowerLimit.toFixed(2) : "—";
  const upper = upperLimit != null ? upperLimit.toFixed(2) : "—";
  const deviationPercent = data.weight_deviation_percent;
  const deviationKg = data.weight_deviation_kg;
  const deviationPercentText = formatDeviation(deviationPercent);
  const deviationKgText = formatDeviation(deviationKg);
  const age = data.age != null ? data.age : "—";
  const heightCm = data.height_cm != null ? data.height_cm : "—";
  const status = data.status || "—";
  const statusType = (data.status_type || "—").toString();
  const restrictions = data.restrictions != null && data.restrictions !== "" ? data.restrictions : null;
  const categoryType = data.category_type;
  
  let reasonText = '';
  let reasonTitle = '';
  
  if (statusClass === 'unauth') {
    reasonTitle = 'Why is this person UNFIT?';
    if (lowerLimit != null && actualWeight != null && actualWeight < lowerLimit) {
      const underweight = (lowerLimit - actualWeight).toFixed(2);
      reasonText = `This person is UNDERWEIGHT by ${underweight} kg (${deviationPercentText}%). Their actual weight (${actualWeight} kg) is below the minimum authorized weight (${lower} kg) for their age (${age} years) and height (${heightCm} cm).`;
    } else if (upperLimit != null && actualWeight != null && actualWeight > upperLimit) {
      const overweight = (actualWeight - upperLimit).toFixed(2);
      reasonText = `This person is OVERWEIGHT by ${overweight} kg (${deviationPercentText}%). Their actual weight (${actualWeight} kg) exceeds the maximum authorized weight (${upper} kg) for their age (${age} years) and height (${heightCm} cm).`;
    } else {
      reasonText = `This person is UNFIT. Their weight (${actualWeight} kg) does not fall within the authorized range (${lower} kg - ${upper} kg) for their age (${age} years) and height (${heightCm} cm).`;
    }
  } else if (statusClass === 'auth') {
    reasonTitle = 'Why is this person FIT?';
    reasonText = `This person's weight (${actualWeight} kg) falls within the authorized range (${lower} kg - ${upper} kg) for their age (${age} years) and height (${heightCm} cm). The ideal weight for this profile is ${ideal} kg.`;
  } else if (statusClass === 'shape') {
    reasonTitle = 'Why is this person in SHAPE I?';
    reasonText = `This person is classified as SHAPE I, which means they are medically fit for all duties. `;
    if (status === 'Fit') {
      reasonText += `Their weight (${actualWeight} kg) is within the authorized range (${lower} kg - ${upper} kg), making them FIT for service.`;
    } else if (status === 'UnFit') {
      reasonText += `However, they are currently UNFIT based on weight criteria. `;
      if (lowerLimit != null && actualWeight != null && actualWeight < lowerLimit) {
        reasonText += `They are UNDERWEIGHT by ${deviationPercentText}% (below ${lower} kg).`;
      } else if (upperLimit != null && actualWeight != null && actualWeight > upperLimit) {
        reasonText += `They are OVERWEIGHT by ${deviationPercentText}% (above ${upper} kg).`;
      }
    }
  } else if (statusClass === 'category') {
    reasonTitle = 'Why is this person in CATEGORY?';
    const catTypeLabel = categoryType ? String(categoryType).charAt(0).toUpperCase() + String(categoryType).slice(1) : 'Unknown';
    reasonText = `This person is classified as CATEGORY (${catTypeLabel}), which means they have medical restrictions or limitations. `;
    if (restrictions) {
      reasonText += `Restrictions: ${restrictions}. `;
    }
    reasonText += `Their current fitness status is: ${status}. `;
    if (status === 'UnFit') {
      reasonText += `They are UNFIT based on weight criteria with a deviation of ${deviationPercentText}%. `;
      if (lowerLimit != null && actualWeight != null && actualWeight < lowerLimit) {
        reasonText += `Their weight (${actualWeight} kg) is below the minimum authorized weight (${lower} kg).`;
      } else if (upperLimit != null && actualWeight != null && actualWeight > upperLimit) {
        reasonText += `Their weight (${actualWeight} kg) exceeds the maximum authorized weight (${upper} kg).`;
      }
    } else if (status === 'Fit') {
      reasonText += `Their weight (${actualWeight} kg) is within the authorized range (${lower} kg - ${upper} kg).`;
    }
  }

  const statusBadgeClass = status === 'Fit' ? 'status-fit' : 'status-unfit';
  const statusTypeBadgeClass = statusType === 'shape' ? 'status-shape' : 'status-category';

  const esc = (s) => (s == null || s === undefined) ? '' : String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  body.innerHTML = `
    <div class="person-details-section">
      <h4>Personal Information</h4>
      <div class="detail-row">
        <div class="detail-label">Army Number:</div>
        <div class="detail-value">${esc(data.army_number)}</div>
      </div>
      <div class="detail-row">
        <div class="detail-label">Name:</div>
        <div class="detail-value">${esc(data.name)}</div>
      </div>
      <div class="detail-row">
        <div class="detail-label">Rank:</div>
        <div class="detail-value">${esc(data.rank)}</div>
      </div>
      <div class="detail-row">
        <div class="detail-label">Company:</div>
        <div class="detail-value">${esc(data.company)}</div>
      </div>
      <div class="detail-row">
        <div class="detail-label">Age:</div>
        <div class="detail-value">${esc(age)} years</div>
      </div>
    </div>
    
    <div class="person-details-section">
      <h4>Physical Measurements</h4>
      <div class="detail-row">
        <div class="detail-label">Height:</div>
        <div class="detail-value">${esc(heightCm)} cm</div>
      </div>
      <div class="detail-row">
        <div class="detail-label">Actual Weight:</div>
        <div class="detail-value"><strong>${esc(actualWeight)} kg</strong></div>
      </div>
      <div class="detail-row">
        <div class="detail-label">Ideal Weight:</div>
        <div class="detail-value">${ideal} kg</div>
      </div>
      <div class="detail-row">
        <div class="detail-label">Authorized Range:</div>
        <div class="detail-value">${lower} kg - ${upper} kg</div>
      </div>
    </div>
    
    <div class="person-details-section">
      <h4>Fitness Status</h4>
      <div class="detail-row">
        <div class="detail-label">Status:</div>
        <div class="detail-value">
          <span class="status-badge-large ${statusBadgeClass}">${esc(status)}</span>
        </div>
      </div>
      <div class="detail-row">
        <div class="detail-label">Status Type:</div>
        <div class="detail-value">
          <span class="status-badge-large ${statusTypeBadgeClass}">${esc(statusType).toUpperCase()}</span>
        </div>
      </div>
      ${categoryType ? `
      <div class="detail-row">
        <div class="detail-label">Category Type:</div>
        <div class="detail-value">${esc(String(categoryType).charAt(0).toUpperCase() + String(categoryType).slice(1))}</div>
      </div>
      ` : ''}
      <div class="detail-row">
        <div class="detail-label">Weight Deviation:</div>
        <div class="detail-value">${deviationKgText} kg (${deviationPercentText}%)</div>
      </div>
    </div>
    
    ${reasonText ? `
    <div class="person-details-section">
      <div class="reason-box">
        <h5>${esc(reasonTitle)}</h5>
        <p>${esc(reasonText)}</p>
      </div>
    </div>
    ` : ''}
    
    ${restrictions ? `
    <div class="person-details-section">
      <h4>Restrictions</h4>
      <div class="reason-box">
        <p>${esc(restrictions)}</p>
      </div>
    </div>
    ` : ''}
  `;
}

function closePersonDetailsModal() {
  const modal = document.getElementById('person-details-modal');
  if (modal) {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
  }
}
window.closePersonDetailsModal = closePersonDetailsModal;

// Direct bindings for modal close - run when DOM is ready so close button always works
function setupPersonDetailsModalClose() {
  const modal = document.getElementById('person-details-modal');
  const closeBtn = document.getElementById('person-details-modal-close');
  if (!modal) return;

  function hideModal() {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
  }

  if (closeBtn) {
    closeBtn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      hideModal();
    });
  }

  modal.addEventListener('click', function (e) {
    if (e.target === modal) {
      hideModal();
    }
  });
}

// Run when DOM is ready (handles module load order)
document.addEventListener('DOMContentLoaded', setupPersonDetailsModalClose);
if (document.readyState !== 'loading') {
  setupPersonDetailsModalClose();
}

// Event delegation for view buttons
document.addEventListener('click', function(event) {
  const viewBtn = event.target.closest('.view-person-btn');
  if (viewBtn) {
    event.preventDefault();
    event.stopPropagation();
    const armyNumber = viewBtn.getAttribute('data-army-number');
    const statusClass = viewBtn.getAttribute('data-status-class');
    if (armyNumber && statusClass && typeof window.showPersonModalWithData === 'function') {
      const row = tableData.find(function(t) { return t.army_number === armyNumber; });
      if (row) {
        window.showPersonModalWithData(row, statusClass);
      }
    }
    return;
  }
});