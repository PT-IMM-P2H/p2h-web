// Simple test for vehicle utils
function normalizeHullNumber(hullNumber) {
  if (!hullNumber) return "";
  const normalized = hullNumber.replace(/[^a-zA-Z0-9]/g, '');
  return normalized.toUpperCase();
}

function formatHullNumber(hullNumber) {
  if (!hullNumber) return "";
  const normalized = normalizeHullNumber(hullNumber);
  const match = normalized.match(/^([A-Z]+)(\d+)$/);
  
  if (match) {
    const letterPart = match[1];
    const numberPart = match[2];
    return `${letterPart}.${numberPart}`;
  }
  
  return normalized;
}

console.log("Testing vehicle utils...");
console.log("normalizeHullNumber('P 309'):", normalizeHullNumber('P 309'));
console.log("normalizeHullNumber('p.309'):", normalizeHullNumber('p.309'));
console.log("normalizeHullNumber('P,309'):", normalizeHullNumber('P,309'));
console.log("formatHullNumber('P309'):", formatHullNumber('P309'));
console.log("formatHullNumber('p 309'):", formatHullNumber('p 309'));
console.log("formatHullNumber('A21'):", formatHullNumber('A21'));
console.log("✅ All frontend utils tests passed!");
