// Form Validation and Auto-formatting
(function() {
    'use strict';

    // CPF Auto-formatting
    function formatCPF(input) {
        let value = input.value.replace(/\D/g, ''); // Remove tudo que não é dígito
        
        if (value.length > 11) {
            value = value.slice(0, 11);
        }
        
        // Aplica a máscara XXX.XXX.XXX-XX
        if (value.length > 9) {
            value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{1,2})/, '$1.$2.$3-$4');
        } else if (value.length > 6) {
            value = value.replace(/(\d{3})(\d{3})(\d{1,3})/, '$1.$2.$3');
        } else if (value.length > 3) {
            value = value.replace(/(\d{3})(\d{1,3})/, '$1.$2');
        }
        
        input.value = value;
    }

    // CPF Validation
    function validateCPF(cpf) {
        cpf = cpf.replace(/\D/g, '');
        
        if (cpf.length !== 11) return false;
        if (/^(\d)\1{10}$/.test(cpf)) return false; // Sequência repetida
        
        // Valida primeiro dígito
        let sum = 0;
        for (let i = 0; i < 9; i++) {
            sum += parseInt(cpf.charAt(i)) * (10 - i);
        }
        let remainder = sum % 11;
        let digit1 = remainder < 2 ? 0 : 11 - remainder;
        
        if (parseInt(cpf.charAt(9)) !== digit1) return false;
        
        // Valida segundo dígito
        sum = 0;
        for (let i = 0; i < 10; i++) {
            sum += parseInt(cpf.charAt(i)) * (11 - i);
        }
        remainder = sum % 11;
        let digit2 = remainder < 2 ? 0 : 11 - remainder;
        
        return parseInt(cpf.charAt(10)) === digit2;
    }

    // Email Domain Validation
    function validateEmailDomain(email) {
        const allowedDomains = ['@gmail.com', '@outlook.com', '@hotmail.com'];
        const emailLower = email.toLowerCase();
        return allowedDomains.some(domain => emailLower.endsWith(domain));
    }

    // Email Characters Validation
    function validateEmailCharacters(email) {
        if (!email.includes('@')) return false;
        const localPart = email.split('@')[0];
        return /^[a-zA-Z0-9._-]+$/.test(localPart);
    }

    // Username Validation
    function validateUsername(username) {
        if (username.length < 8) return false;
        if (!/^[a-zA-Z0-9]+$/.test(username)) return false;
        if (!/[a-zA-Z]/.test(username)) return false;
        return true;
    }

    // Password Validation
    function validatePassword(password) {
        if (password.length < 8) return false;
        if (!/[a-zA-Z]/.test(password)) return false;
        if (!/\d/.test(password)) return false;
        return true;
    }

    // Show validation message
    function showValidationMessage(input, message, isError = true) {
        // Remove mensagem anterior
        const existingMsg = input.parentElement.querySelector('.validation-message');
        if (existingMsg) {
            existingMsg.remove();
        }
        
        if (message) {
            const msgDiv = document.createElement('div');
            msgDiv.className = `validation-message ${isError ? 'text-danger' : 'text-success'} small mt-1`;
            msgDiv.textContent = message;
            input.parentElement.appendChild(msgDiv);
        }
    }

    // Initialize form validation
    document.addEventListener('DOMContentLoaded', function() {
        const cpfInput = document.getElementById('id_cpf');
        const emailInput = document.getElementById('id_email');
        const usernameInput = document.getElementById('id_username');
        const password1Input = document.getElementById('id_password1');
        const password2Input = document.getElementById('id_password2');

        // CPF auto-formatting
        if (cpfInput) {
            cpfInput.addEventListener('input', function(e) {
                formatCPF(e.target);
            });

            cpfInput.addEventListener('blur', function(e) {
                const cpf = e.target.value;
                if (cpf) {
                    if (!validateCPF(cpf)) {
                        showValidationMessage(e.target, 'CPF inválido.', true);
                        e.target.classList.add('is-invalid');
                        e.target.classList.remove('is-valid');
                    } else {
                        showValidationMessage(e.target, '', false);
                        e.target.classList.remove('is-invalid');
                        e.target.classList.add('is-valid');
                    }
                }
            });

            // Bloqueia caracteres não numéricos
            cpfInput.addEventListener('keypress', function(e) {
                if (!/\d/.test(e.key) && !['Backspace', 'Delete', 'Tab', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
                    e.preventDefault();
                }
            });
        }

        // Email validation
        if (emailInput) {
            emailInput.addEventListener('blur', function(e) {
                const email = e.target.value;
                if (email) {
                    if (!validateEmailCharacters(email)) {
                        showValidationMessage(e.target, 'O e-mail pode conter apenas letras, números, pontos (.), hífens (-) e underscores (_).', true);
                        e.target.classList.add('is-invalid');
                        e.target.classList.remove('is-valid');
                    } else if (!validateEmailDomain(email)) {
                        showValidationMessage(e.target, 'Somente e-mails com os domínios @gmail.com, @outlook.com e @hotmail.com são aceitos.', true);
                        e.target.classList.add('is-invalid');
                        e.target.classList.remove('is-valid');
                    } else {
                        showValidationMessage(e.target, '', false);
                        e.target.classList.remove('is-invalid');
                        e.target.classList.add('is-valid');
                    }
                }
            });
        }

        // Username validation
        if (usernameInput) {
            usernameInput.addEventListener('input', function(e) {
                const username = e.target.value;
                
                // Valida caracteres em tempo real
                if (username && !/^[a-zA-Z0-9]*$/.test(username)) {
                    const lastChar = username.slice(-1);
                    if (!/[a-zA-Z0-9]/.test(lastChar)) {
                        showValidationMessage(e.target, 'Apenas letras e números são permitidos.', true);
                    }
                } else {
                    showValidationMessage(e.target, '', false);
                }
            });

            usernameInput.addEventListener('blur', function(e) {
                const username = e.target.value;
                if (username) {
                    if (!validateUsername(username)) {
                        if (username.length < 8) {
                            showValidationMessage(e.target, 'O nome de usuário deve ter no mínimo 8 caracteres.', true);
                        } else if (!/^[a-zA-Z0-9]+$/.test(username)) {
                            showValidationMessage(e.target, 'Apenas letras e números são permitidos.', true);
                        } else if (!/[a-zA-Z]/.test(username)) {
                            showValidationMessage(e.target, 'O nome de usuário deve conter pelo menos uma letra.', true);
                        }
                        e.target.classList.add('is-invalid');
                        e.target.classList.remove('is-valid');
                    } else {
                        showValidationMessage(e.target, '', false);
                        e.target.classList.remove('is-invalid');
                        e.target.classList.add('is-valid');
                    }
                }
            });
        }

        // Password validation
        if (password1Input) {
            password1Input.addEventListener('blur', function(e) {
                const password = e.target.value;
                if (password) {
                    if (!validatePassword(password)) {
                        let messages = [];
                        if (password.length < 8) messages.push('mínimo 8 caracteres');
                        if (!/[a-zA-Z]/.test(password)) messages.push('pelo menos uma letra');
                        if (!/\d/.test(password)) messages.push('pelo menos um número');
                        
                        showValidationMessage(e.target, `A senha deve conter: ${messages.join(', ')}.`, true);
                        e.target.classList.add('is-invalid');
                        e.target.classList.remove('is-valid');
                    } else {
                        showValidationMessage(e.target, '', false);
                        e.target.classList.remove('is-invalid');
                        e.target.classList.add('is-valid');
                    }
                }
            });
        }

        // Password confirmation validation
        if (password2Input && password1Input) {
            password2Input.addEventListener('blur', function(e) {
                const password2 = e.target.value;
                const password1 = password1Input.value;
                if (password2) {
                    if (password2 !== password1) {
                        showValidationMessage(e.target, 'As senhas não coincidem.', true);
                        e.target.classList.add('is-invalid');
                        e.target.classList.remove('is-valid');
                    } else {
                        showValidationMessage(e.target, '', false);
                        e.target.classList.remove('is-invalid');
                        e.target.classList.add('is-valid');
                    }
                }
            });
        }
    });
})();
