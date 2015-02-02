;; -*- coding: utf-8 -*-

(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(column-number-mode t)
 '(flycheck-display-errors-function (function flycheck-pos-tip-error-messages))
 '(inhibit-startup-screen t)
 '(show-paren-mode t)
 '(tool-bar-mode nil)
 '(tooltip-mode nil)
 '(menu-bar-mode nil))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(default ((t (:family "Ricty" :foundry "unknown" :slant normal :weight normal :height 120 :width normal)))))


(add-to-list 'load-path "/home/hiroaki/.emacs.d/")
(require 'auto-complete-config)
(add-to-list 'ac-dictionary-directories "/home/hiroaki/.emacs.d//ac-dict")
(ac-config-default)

(deftheme evenhold
  "Face colors using a dark blue background.")

(let ((class '((class color) (min-colors 209))))
  (custom-theme-set-faces
   'evenhold
   `(Info-title-1-face ((,class (:family "helv" :weight bold :height 1.728))))
   `(Info-title-2-face ((,class (:family "helv" :weight bold :height 1.44))))
   `(Info-title-3-face ((,class (:family "helv" :weight bold :height 1.2))))
   `(Info-title-4-face ((,class (:family "helv" :weight bold))))
   `(compilation-column-number ((,class (:foreground "LightGreen"))))
   `(compilation-error ((,class (:foreground "Red1"))))
   `(compilation-info ((,class (:weight normal :foreground "LightSkyBlue"))))
   `(compilation-line-number ((,class (:foreground "LightGreen"))))
   `(compilation-mode-line-exit ((,class (:foreground "blue4"))))
   `(cperl-array-face ((,class (:foreground "yellow2"))))
   `(cperl-hash-face ((,class (:foreground "green"))))
   `(cursor ((,class (:background "#34ADF2"))))
   `(default ((,class (:background "#000000" :foreground "#D0D0D0")))) 
   `(diff-added ((,class (nil))))
   `(diff-changed ((,class (nil))))
   `(diff-context ((,class (:foreground "seashell4"))))
   `(diff-file-header ((,class (:background "grey60"))))
   `(diff-function ((,class (:inherit diff-header))))
   `(diff-header ((,class (:background "grey45"))))
   `(diff-hunk-header ((,class (:inherit diff-header))))
   `(diff-index ((,class (:inherit diff-file-header))))
   `(diff-indicator-added ((,class (:foreground "white" :background "darkolivegreen"))))
   `(diff-indicator-changed ((,class (:foreground "white" :background "dodgerblue4"))))
   `(diff-indicator-removed ((,class (:foreground "white" :background "indianred4"))))
   `(diff-refine-change ((,class (:background "skyblue4"))))
   `(diff-removed ((,class (nil))))
   `(dired-marked ((,class (:background "dodgerblue3" :foreground "white"))))
   `(ediff-current-diff-A ((,class (:background "green4" :foreground "white"))))
   `(ediff-current-diff-B ((,class (:background "darkorange3" :foreground "white"))))
   `(ediff-even-diff-B ((,class (:background "Grey50" :foreground "White"))))
   `(ediff-fine-diff-A ((,class (:background "skyblue4" :foreground "white"))))
   `(ediff-fine-diff-B ((,class (:background "cyan4" :foreground "white"))))
   `(ediff-odd-diff-A ((,class (:background "Grey50" :foreground "White"))))
   `(error ((,class (:foreground "#BB0000")))) 
   `(flymake-errline ((,class (:background nil :underline "red"))))
   `(flymake-warnline ((,class (:background nil :underline "green"))))
   `(font-lock-builtin-face ((,class (:foreground "#FF983C" :weight bold))))
   `(font-lock-comment-delimiter-face ((,class (:foreground "#A5A6A6")))) 
   `(font-lock-comment-face ((,class (:foreground "#626262"))))
   `(font-lock-constant-face ((,class (:foreground "#C61A1A"))))
   `(font-lock-doc-face ((,class (:foreground "#EFEFEF"))))
   `(font-lock-doc-string-face ((,class (:foreground "moccasin"))))
   `(font-lock-function-name-face ((,class (:foreground "#32BAFF" ))))
   `(font-lock-keyword-face ((,class (:foreground "#8600AF" ))))
   `(font-lock-preprocessor-face ((,class (:foreground "#007DC5"))))
   `(font-lock-reference-face ((,class (:foreground "green"))))
   `(font-lock-regexp-grouping-backslash ((,class (:weight bold))))
   `(font-lock-regexp-grouping-construct ((,class (:weight bold))))
   `(font-lock-string-face ((,class (:foreground "#0097BD"))))
   `(font-lock-type-face ((,class (:foreground "#FF983C" :weight bold ))))
   `(font-lock-variable-name-face ((,class (:foreground "#53E3FF" :weight bold))))
   `(fringe ((,class (:background "#000000"))))
   `(highlight ((,class (:background "DodgerBlue4"))))
   `(ido-first-match ((,class (:weight normal :foreground "orange"))))
   `(ido-only-match ((,class (:foreground "green"))))
   `(ido-subdir ((,class (:foreground nil :inherit font-lock-keyword-face))))
   `(info-header-node ((,class (:foreground "DeepSkyBlue1"))))
   `(info-header-xref ((,class (:foreground "SeaGreen2"))))
   `(info-menu-header ((,class (:family "helv" :weight bold))))
   `(info-node ((,class (:foreground "DeepSkyBlue1"))))
   `(info-xref ((,class (:foreground "SeaGreen2"))))
   `(isearch ((,class (:background "coral2" :foreground "white"))))
   `(isearch-lazy-highlight-face ((,class (:background "coral4" :foreground "white"))))
   `(lazy-highlight ((,class (:background "cadetblue" :foreground "white"))))
   `(match ((,class (:background "DeepPink4"))))
   `(minibuffer-prompt ((,class (:foreground "#00A2CF"))))
   `(mode-line ((,class (:background "#004A63" :foreground "#F2F2F2" :box (:line-width 1 :color "#004A63":style released-button)))))
   `(mode-line-buffer-id ((,class (:weight bold :background nil :foreground "#2CF5FF" ))))
   `(mode-line-inactive ((,class (:background "black" :foreground "#00A3CC" :box (:line-width 1 :color "#009AC0" :style nil)))))
   `(outline-1 ((,class (:foreground "SkyBlue1"))))
   `(outline-2 ((,class (:foreground "CadetBlue1"))))
   `(outline-3 ((,class (:foreground "LightSteelBlue1"))))
   `(outline-4 ((,class (:foreground "turquoise2"))))
   `(outline-5 ((,class (:foreground "aquamarine1"))))
   `(primary-selection ((,class (:background "blue3"))))
   `(region ((,class (:background "#103050"))))
   `(show-paren-match-face ((,class (:background "dodgerblue1" :foreground "white"))))
   `(show-paren-mismatch-face ((,class (:background "red" :foreground "white"))))
   `(success ((,class (:foreground "SeaGreen2"))))
   `(warning ((,class (:foreground "Yellow"))))))

(provide-theme 'evenhold)

;; Local Variables:
;; no-byte-compile: t
;; End:

;;; evenhold-theme.el ends here


;;;行番号と列番号
(line-number-mode t)
(column-number-mode t)

;;;カッコをハイライト
(show-paren-mode t)

;; カーソル行に下線を表示
(setq hl-line-face 'underline)
(global-hl-line-mode)


;;; MELPA関連
(require 'package)

;; MELPAを追加
(add-to-list 'package-archives '("melpa" . "http://melpa.milkbox.net/packages/"))

;; Marmaladeを追加
(add-to-list 'package-archives  '("marmalade" . "http://marmalade-repo.org/packages/"))

;; 初期化
(package-initialize)


;;flycheck
(add-hook 'after-init-hook #'global-flycheck-mode)

(eval-after-load 'flycheck
  '(custom-set-variables
   '(flycheck-display-errors-function #'flycheck-pos-tip-error-messages)))


;;magit
(require 'magit)

;;;スクロールバー非表示
(scroll-bar-mode 0)

;;;起動時画面分割
(setq w (selected-window))
(setq w3 (split-window w 70 t))

;;; cython-mode.el --- Major mode for editing Cython files

;;; Commentary:

;; This should work with python-mode.el as well as either the new
;; python.el or the old.

;;; Code:

;; Load python-mode if available, otherwise use builtin emacs python package
(when (not (require 'python-mode nil t))
  (require 'python))
(eval-when-compile (require 'rx))

;;;###autoload
(add-to-list 'auto-mode-alist '("\\.pyx\\'" . cython-mode))
;;;###autoload
(add-to-list 'auto-mode-alist '("\\.pxd\\'" . cython-mode))
;;;###autoload
(add-to-list 'auto-mode-alist '("\\.pxi\\'" . cython-mode))


(defvar cython-buffer nil
  "Variable pointing to the cython buffer which was compiled.")

(defun cython-compile ()
  "Compile the file via Cython."
  (interactive)
  (let ((cy-buffer (current-buffer)))
    (with-current-buffer
        (compile compile-command)
      (set (make-local-variable 'cython-buffer) cy-buffer)
      (add-to-list (make-local-variable 'compilation-finish-functions)
                   'cython-compilation-finish))))

(defun cython-compilation-finish (buffer how)
  "Called when Cython compilation finishes."
  ;; XXX could annotate source here
  )

(defvar cython-mode-map
  (let ((map (make-sparse-keymap)))
    ;; Will inherit from `python-mode-map' thanks to define-derived-mode.
    (define-key map "\C-c\C-c" 'cython-compile)
    map)
  "Keymap used in `cython-mode'.")

(defvar cython-font-lock-keywords
  `(;; ctypedef statement: "ctypedef (...type... alias)?"
    (,(rx
       ;; keyword itself
       symbol-start (group "ctypedef")
       ;; type specifier: at least 1 non-identifier symbol + 1 identifier
       ;; symbol and anything but a comment-starter after that.
       (opt (regexp "[^a-zA-z0-9_\n]+[a-zA-Z0-9_][^#\n]*")
            ;; type alias: an identifier
            symbol-start (group (regexp "[a-zA-Z_]+[a-zA-Z0-9_]*"))
            ;; space-or-comments till the end of the line
            (* space) (opt "#" (* nonl)) line-end))
     (1 font-lock-keyword-face)
     (2 font-lock-type-face nil 'noerror))
    ;; new keywords in Cython language
    (,(rx symbol-start
          (or "by" "cdef" "cimport" "cpdef"
              "extern" "gil" "include" "nogil" "property" "public"
              "readonly" "DEF" "IF" "ELIF" "ELSE"
              "new" "del" "cppclass" "namespace" "const"
              "__stdcall" "__cdecl" "__fastcall" "inline" "api")
          symbol-end)
     . font-lock-keyword-face)
    ;; Question mark won't match at a symbol-end, so 'except?' must be
    ;; special-cased.  It's simpler to handle it separately than weaving it
    ;; into the lengthy list of other keywords.
    (,(rx symbol-start "except?") . font-lock-keyword-face)
    ;; C and Python types (highlight as builtins)
    (,(rx symbol-start
          (or
           "object" "dict" "list"
           ;; basic c type names
           "void" "char" "int" "float" "double" "bint"
           ;; longness/signed/constness
           "signed" "unsigned" "long" "short"
           ;; special basic c types
           "size_t" "Py_ssize_t" "Py_UNICODE" "Py_UCS4" "ssize_t" "ptrdiff_t")
          symbol-end)
     . font-lock-builtin-face)
    (,(rx symbol-start "NULL" symbol-end)
     . font-lock-constant-face)
    ;; cdef is used for more than functions, so simply highlighting the next
    ;; word is problematic. struct, enum and property work though.
    (,(rx symbol-start
          (group (or "struct" "enum" "union"
                     (seq "ctypedef" (+ space "fused"))))
          (+ space) (group (regexp "[a-zA-Z_]+[a-zA-Z0-9_]*")))
     (1 font-lock-keyword-face prepend) (2 font-lock-type-face))
    ("\\_<property[ \t]+\\([a-zA-Z_]+[a-zA-Z0-9_]*\\)"
     1 font-lock-function-name-face))
  "Additional font lock keywords for Cython mode.")

;;;###autoload
(defgroup cython nil "Major mode for editing and compiling Cython files"
  :group 'languages
  :prefix "cython-"
  :link '(url-link :tag "Homepage" "http://cython.org"))

;;;###autoload
(defcustom cython-default-compile-format "cython -a %s"
  "Format for the default command to compile a Cython file.
It will be passed to `format' with `buffer-file-name' as the only other argument."
  :group 'cython
  :type 'string)

;; Some functions defined differently in the different python modes
(defun cython-comment-line-p ()
  "Return non-nil if current line is a comment."
  (save-excursion
    (back-to-indentation)
    (eq ?# (char-after (point)))))

(defun cython-in-string/comment ()
  "Return non-nil if point is in a comment or string."
  (nth 8 (syntax-ppss)))

(defalias 'cython-beginning-of-statement
  (cond
   ;; python-mode.el
   ((fboundp 'py-beginning-of-statement)
    'py-beginning-of-statement)
   ;; old python.el
   ((fboundp 'python-beginning-of-statement)
    'python-beginning-of-statement)
   ;; new python.el
   ((fboundp 'python-nav-beginning-of-statement)
    'python-nav-beginning-of-statement)
   (t (error "Couldn't find implementation for `cython-beginning-of-statement'"))))

(defalias 'cython-beginning-of-block
  (cond
   ;; python-mode.el
   ((fboundp 'py-beginning-of-block)
    'py-beginning-of-block)
   ;; old python.el
   ((fboundp 'python-beginning-of-block)
    'python-beginning-of-block)
   ;; new python.el
   ((fboundp 'python-nav-beginning-of-block)
    'python-nav-beginning-of-block)
   (t (error "Couldn't find implementation for `cython-beginning-of-block'"))))

(defalias 'cython-end-of-statement
  (cond
   ;; python-mode.el
   ((fboundp 'py-end-of-statement)
    'py-end-of-statement)
   ;; old python.el
   ((fboundp 'python-end-of-statement)
    'python-end-of-statement)
   ;; new python.el
   ((fboundp 'python-nav-end-of-statement)
    'python-nav-end-of-statement)
   (t (error "Couldn't find implementation for `cython-end-of-statement'"))))

(defun cython-open-block-statement-p (&optional bos)
  "Return non-nil if statement at point opens a Cython block.
BOS non-nil means point is known to be at beginning of statement."
  (save-excursion
    (unless bos (cython-beginning-of-statement))
    (looking-at (rx (and (or "if" "else" "elif" "while" "for" "def" "cdef" "cpdef"
                             "class" "try" "except" "finally" "with"
                             "EXAMPLES:" "TESTS:" "INPUT:" "OUTPUT:")
                         symbol-end)))))

(defun cython-beginning-of-defun ()
  "`beginning-of-defun-function' for Cython.
Finds beginning of innermost nested class or method definition.
Returns the name of the definition found at the end, or nil if
reached start of buffer."
  (let ((ci (current-indentation))
        (def-re (rx line-start (0+ space) (or "def" "cdef" "cpdef" "class") (1+ space)
                    (group (1+ (or word (syntax symbol))))))
        found lep) ;; def-line
    (if (cython-comment-line-p)
        (setq ci most-positive-fixnum))
    (while (and (not (bobp)) (not found))
      ;; Treat bol at beginning of function as outside function so
      ;; that successive C-M-a makes progress backwards.
      ;;(setq def-line (looking-at def-re))
      (unless (bolp) (end-of-line))
      (setq lep (line-end-position))
      (if (and (re-search-backward def-re nil 'move)
               ;; Must be less indented or matching top level, or
               ;; equally indented if we started on a definition line.
               (let ((in (current-indentation)))
                 (or (and (zerop ci) (zerop in))
                     (= lep (line-end-position)) ; on initial line
                     ;; Not sure why it was like this -- fails in case of
                     ;; last internal function followed by first
                     ;; non-def statement of the main body.
                     ;;(and def-line (= in ci))
                     (= in ci)
                     (< in ci)))
               (not (cython-in-string/comment)))
          (setq found t)))))

(defun cython-end-of-defun ()
  "`end-of-defun-function' for Cython.
Finds end of innermost nested class or method definition."
  (let ((orig (point))
        (pattern (rx line-start (0+ space) (or "def" "cdef" "cpdef" "class") space)))
    ;; Go to start of current block and check whether it's at top
    ;; level.  If it is, and not a block start, look forward for
    ;; definition statement.
    (when (cython-comment-line-p)
      (end-of-line)
      (forward-comment most-positive-fixnum))
    (when (not (cython-open-block-statement-p))
      (cython-beginning-of-block))
    (if (zerop (current-indentation))
        (unless (cython-open-block-statement-p)
          (while (and (re-search-forward pattern nil 'move)
                      (cython-in-string/comment))) ; just loop
          (unless (eobp)
            (beginning-of-line)))
      ;; Don't move before top-level statement that would end defun.
      (end-of-line)
      (beginning-of-defun))
    ;; If we got to the start of buffer, look forward for
    ;; definition statement.
    (when (and (bobp) (not (looking-at (rx (or "def" "cdef" "cpdef" "class")))))
      (while (and (not (eobp))
                  (re-search-forward pattern nil 'move)
                  (cython-in-string/comment)))) ; just loop
    ;; We're at a definition statement (or end-of-buffer).
    ;; This is where we should have started when called from end-of-defun
    (unless (eobp)
      (let ((block-indentation (current-indentation)))
        (python-nav-end-of-statement)
        (while (and (forward-line 1)
                    (not (eobp))
                    (or (and (> (current-indentation) block-indentation)
                             (or (cython-end-of-statement) t))
                        ;; comment or empty line
                        (looking-at (rx (0+ space) (or eol "#"))))))
        (forward-comment -1))
      ;; Count trailing space in defun (but not trailing comments).
      (skip-syntax-forward " >")
      (unless (eobp)			; e.g. missing final newline
        (beginning-of-line)))
    ;; Catch pathological cases like this, where the beginning-of-defun
    ;; skips to a definition we're not in:
    ;; if ...:
    ;;     ...
    ;; else:
    ;;     ...  # point here
    ;;     ...
    ;;     def ...
    (if (< (point) orig)
        (goto-char (point-max)))))

(defun cython-current-defun ()
  "`add-log-current-defun-function' for Cython."
  (save-excursion
    ;; Move up the tree of nested `class' and `def' blocks until we
    ;; get to zero indentation, accumulating the defined names.
    (let ((start t)
          accum)
      (while (or start (> (current-indentation) 0))
        (setq start nil)
        (cython-beginning-of-block)
        (end-of-line)
        (beginning-of-defun)
        (if (looking-at (rx (0+ space) (or "def" "cdef" "cpdef" "class") (1+ space)
                            (group (1+ (or word (syntax symbol))))))
            (push (match-string 1) accum)))
      (if accum (mapconcat 'identity accum ".")))))

;;;###autoload
(define-derived-mode cython-mode python-mode "Cython"
  "Major mode for Cython development, derived from Python mode.
\\{cython-mode-map}"
  (font-lock-add-keywords nil cython-font-lock-keywords)
  (set (make-local-variable 'outline-regexp)
       (rx (* space) (or "class" "def" "cdef" "cpdef" "elif" "else" "except" "finally"
                         "for" "if" "try" "while" "with")
           symbol-end))
  (set (make-local-variable 'beginning-of-defun-function)
       #'cython-beginning-of-defun)
  (set (make-local-variable 'end-of-defun-function)
       #'cython-end-of-defun)
  (set (make-local-variable 'compile-command)
       (format cython-default-compile-format (shell-quote-argument buffer-file-name)))
  (set (make-local-variable 'add-log-current-defun-function)
       #'cython-current-defun)
  (add-hook 'which-func-functions #'cython-current-defun nil t)
  (add-to-list (make-local-variable 'compilation-finish-functions)
               'cython-compilation-finish))

(provide 'cython-mode)

;;; cython-mode.el ends here
