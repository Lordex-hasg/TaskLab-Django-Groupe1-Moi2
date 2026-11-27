from django.test import TestCase
from django.urls import reverse
from .models import Tache
from .forms import TacheForm

class TacheTests(TestCase):
    def test_creation_modele(self):
        tache = Tache.objects.create(titre="Réviser Django")
        self.assertEqual(str(tache), "Réviser Django")

    def test_liste_accessible(self):
        response = self.client.get(reverse("liste_taches"))
        self.assertEqual(response.status_code, 200)

    def test_creation_formulaire_valide(self):
        form = TacheForm(
            data={
                "titre": "Réviser Django",
                "description": "Préparer le TP",
                "statut": "A_FAIRE",
                "priorite": 2,
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        tache = form.save()
        self.assertEqual(Tache.objects.get(pk=tache.pk).titre, "Réviser Django")

    def test_validation_priorite(self):
        donnees = {
            "titre": "Priorité à vérifier",
            "description": "",
            "statut": "A_FAIRE",
        }

        for priorite in (0, 4):
            with self.subTest(priorite=priorite):
                form = TacheForm(data={**donnees, "priorite": priorite})
                self.assertFalse(form.is_valid())
                self.assertIn("priorite", form.errors)

        for priorite in (1, 3):
            with self.subTest(priorite=priorite):
                form = TacheForm(data={**donnees, "priorite": priorite})
                self.assertTrue(form.is_valid(), form.errors)

    def test_creation_par_post(self):
        response = self.client.post(
            reverse("creer_tache"),
            {
                "titre": "Nouvelle tâche",
                "description": "Créée depuis le formulaire",
                "statut": "A_FAIRE",
                "priorite": 1,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tache.objects.filter(titre="Nouvelle tâche").exists())

    def test_suppression_par_post(self):
        tache = Tache.objects.create(titre="Tâche à supprimer")

        response = self.client.post(reverse("supprimer_tache", args=[tache.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Tache.objects.filter(pk=tache.pk).exists())
