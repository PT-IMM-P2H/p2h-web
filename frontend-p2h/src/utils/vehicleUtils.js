/**
 * Vehicle Utils - Utility functions untuk pemrosesan data kendaraan
 */

/**
 * Normalize nomor lambung untuk searching dan comparison
 * Menghapus spasi, titik, koma, dan karakter khusus lainnya
 * Convert ke uppercase
 * 
 * @param {string} hullNumber - Nomor lambung dalam format apapun
 * @returns {string} Normalized hull number (uppercase, tanpa separator)
 * 
 * @example
 * normalizeHullNumber("P 309") // "P309"
 * normalizeHullNumber("p.309") // "P309"
 * normalizeHullNumber("P,309") // "P309"
 * normalizeHullNumber("  P  .  309  ") // "P309"
 */
export function normalizeHullNumber(hullNumber) {
  if (!hullNumber) return "";
  
  // Hapus spasi, titik, koma, dash, dan karakter khusus lainnya
  // Hanya keep alphanumeric
  const normalized = hullNumber.replace(/[^a-zA-Z0-9]/g, '');
  
  // Convert ke uppercase
  return normalized.toUpperCase();
}

/**
 * Format nomor lambung ke format standar: [HURUF].[ANGKA]
 * 
 * @param {string} hullNumber - Nomor lambung dalam format apapun
 * @returns {string} Formatted hull number dengan titik separator
 * 
 * @example
 * formatHullNumber("P309") // "P.309"
 * formatHullNumber("A21") // "A.21"
 * formatHullNumber("p 309") // "P.309"
 * formatHullNumber("P,309") // "P.309"
 */
export function formatHullNumber(hullNumber) {
  if (!hullNumber) return "";
  
  // Normalize dulu untuk clean the input
  const normalized = normalizeHullNumber(hullNumber);
  
  // Extract letter prefix dan number part
  // Asumsikan format: satu atau lebih huruf diikuti angka
  const match = normalized.match(/^([A-Z]+)(\d+)$/);
  
  if (match) {
    const letterPart = match[1];
    const numberPart = match[2];
    return `${letterPart}.${numberPart}`;
  }
  
  // Jika tidak match pattern, return normalized value
  return normalized;
}

/**
 * Validate format nomor lambung
 * Format yang valid: huruf + angka (bisa dengan atau tanpa separator)
 * 
 * @param {string} hullNumber - Nomor lambung untuk divalidasi
 * @returns {{isValid: boolean, errorMessage: string|null}} Hasil validasi
 * 
 * @example
 * validateHullNumberFormat("P309") // { isValid: true, errorMessage: null }
 * validateHullNumberFormat("P.309") // { isValid: true, errorMessage: null }
 * validateHullNumberFormat("123") // { isValid: false, errorMessage: "..." }
 */
export function validateHullNumberFormat(hullNumber) {
  if (!hullNumber) {
    return {
      isValid: false,
      errorMessage: "Nomor lambung tidak boleh kosong"
    };
  }
  
  // Normalize untuk validasi
  const normalized = normalizeHullNumber(hullNumber);
  
  // Check jika kosong setelah normalisasi
  if (!normalized) {
    return {
      isValid: false,
      errorMessage: "Nomor lambung tidak valid (hanya berisi karakter khusus)"
    };
  }
  
  // Check format: harus ada huruf dan angka
  if (!/^[A-Z]+\d+$/.test(normalized)) {
    return {
      isValid: false,
      errorMessage: "Format nomor lambung harus: huruf + angka (contoh: P309, A21, B030)"
    };
  }
  
  return {
    isValid: true,
    errorMessage: null
  };
}

/**
 * Auto-format input nomor lambung saat user mengetik
 * Untuk digunakan di input handler
 * 
 * @param {string} value - Input value dari user
 * @param {boolean} formatOnTheFly - Jika true, format langsung. Jika false, hanya normalize
 * @returns {string} Formatted atau normalized value
 * 
 * @example
 * // Di input handler:
 * formData.value.no_lambung = autoFormatHullNumberInput(event.target.value, false);
 */
export function autoFormatHullNumberInput(value, formatOnTheFly = false) {
  if (!value) return "";
  
  if (formatOnTheFly) {
    // Format langsung saat mengetik (mungkin mengganggu UX)
    return formatHullNumber(value);
  } else {
    // Hanya uppercase dan hapus karakter aneh
    // Tapi keep titik untuk user experience
    return value.toUpperCase();
  }
}

/**
 * Format nomor lambung saat blur (user selesai input)
 * 
 * @param {string} value - Input value dari user
 * @returns {string} Formatted value
 */
export function formatHullNumberOnBlur(value) {
  return formatHullNumber(value);
}
