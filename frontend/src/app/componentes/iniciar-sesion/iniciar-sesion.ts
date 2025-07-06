import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { AuthService } from '../../services/usuario';
import { ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-iniciar-sesion',
  standalone: true,
  templateUrl: './iniciar-sesion.html',
  imports: [ReactiveFormsModule],
})
export class LoginComponent {
  form: FormGroup;

  constructor(private fb: FormBuilder, private auth: AuthService) {
    this.form = this.fb.group({
      username: [''],
      password: ['']
    });
  }

  iniciarSesion() {
    this.auth.login(this.form.value).subscribe({
      next: (res: any) => {
        this.auth.guardarToken(res.access);
        console.log('Sesión iniciada');
      },
      error: err => console.error('Error al iniciar sesión', err)
    });
  }
}
