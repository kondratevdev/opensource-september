const elements = {
  body: document.querySelector('#leaderboard-body'),
  loading: document.querySelector('#loading-state'),
  empty: document.querySelector('#empty-state'),
  error: document.querySelector('#error-state'),
  search: document.querySelector('#project-search'),
  updated: document.querySelector('#last-updated'),
  totalProjects: document.querySelector('#total-projects'),
  totalClosed: document.querySelector('#total-closed'),
  totalOpen: document.querySelector('#total-open'),
  totalUnassigned: document.querySelector('#total-unassigned'),
};

const numberFormatter = new Intl.NumberFormat('en');
const dateFormatter = new Intl.DateTimeFormat('en', {
  day: 'numeric',
  month: 'short',
  year: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
  timeZoneName: 'short',
});

let projects = [];

function makeElement(tagName, className, text) {
  const element = document.createElement(tagName);
  if (className) element.className = className;
  if (text !== undefined) element.textContent = text;
  return element;
}

function renderRank(rank) {
  const className = rank <= 3 ? 'rank rank-highlighted' : 'rank';
  return makeElement('span', className, rank);
}

function renderProject(project, rank) {
  const row = document.createElement('tr');

  const rankCell = document.createElement('td');
  rankCell.append(renderRank(rank));

  const projectCell = document.createElement('td');
  const projectContent = makeElement('div', 'project-cell');
  const avatar = makeElement('img', 'project-avatar');
  avatar.src = project.repository.owner_avatar_url;
  avatar.alt = '';
  avatar.width = 42;
  avatar.height = 42;
  avatar.loading = 'lazy';
  const projectDetails = document.createElement('div');
  projectDetails.append(
    makeElement('span', 'project-name', project.repository.full_name),
    makeElement(
      'span',
      'project-meta',
      `${numberFormatter.format(project.issues)} total · ${numberFormatter.format(project.unassigned_issues)} unassigned`,
    ),
  );
  projectContent.append(avatar, projectDetails);
  projectCell.append(projectContent);

  const progressCell = makeElement('td', 'progress-cell');
  const completion = project.issues === 0
    ? 0
    : Math.round((project.closed_issues / project.issues) * 100);
  const progressLabel = makeElement('div', 'progress-label');
  progressLabel.append(
    makeElement('span', '', 'Completion'),
    makeElement('span', '', `${completion}%`),
  );
  const progressTrack = makeElement('div', 'progress-track');
  const progressValue = makeElement('div', 'progress-value');
  progressValue.style.width = `${completion}%`;
  progressTrack.append(progressValue);
  progressCell.append(progressLabel, progressTrack);

  const closedCell = makeElement(
    'td',
    'metric-number',
    numberFormatter.format(project.closed_issues),
  );
  const openCell = makeElement(
    'td',
    'metric-number metric-number-open',
    numberFormatter.format(project.open_issues),
  );

  const actionCell = makeElement('td', 'action-column');
  const link = makeElement('a', 'project-link', '→');
  link.href = project.repository.url;
  link.target = '_blank';
  link.rel = 'noreferrer';
  link.setAttribute('aria-label', `Open ${project.repository.full_name} on GitHub`);
  actionCell.append(link);

  row.append(rankCell, projectCell, progressCell, closedCell, openCell, actionCell);
  return row;
}

function renderProjects(query = '') {
  const normalizedQuery = query.trim().toLocaleLowerCase();
  const filteredProjects = projects.filter((project) => (
    project.repository.full_name.toLocaleLowerCase().includes(normalizedQuery)
  ));

  elements.body.replaceChildren(
    ...filteredProjects.map((project) => (
      renderProject(project, projects.indexOf(project) + 1)
    )),
  );
  elements.empty.hidden = filteredProjects.length > 0;
}

function renderTotals(report) {
  const { totals } = report;
  elements.totalProjects.textContent = numberFormatter.format(totals.repositories);
  elements.totalClosed.textContent = numberFormatter.format(totals.closed_issues);
  elements.totalOpen.textContent = numberFormatter.format(totals.open_issues);
  elements.totalUnassigned.textContent = numberFormatter.format(totals.unassigned_issues);
  elements.updated.textContent = `Updated ${dateFormatter.format(new Date(report.generated_at))}`;
}

async function loadReport() {
  try {
    const response = await fetch('./project_report.json', { cache: 'no-store' });
    if (!response.ok) throw new Error(`Report request failed: ${response.status}`);

    const report = await response.json();
    projects = report.projects;
    renderTotals(report);
    renderProjects();
    elements.loading.hidden = true;
  } catch (error) {
    console.error(error);
    elements.loading.hidden = true;
    elements.error.hidden = false;
  }
}

elements.search.addEventListener('input', (event) => {
  renderProjects(event.currentTarget.value);
});

loadReport();
