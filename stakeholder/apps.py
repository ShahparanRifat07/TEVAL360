from django.apps import AppConfig



class StakeholderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stakeholder'

    def ready(self):
        import stakeholder.signals
        from evaluation.models import StakeholderTag, InstitutionTag

        if not StakeholderTag.objects.exists():
            # Create initial instances of MyModel
            student = StakeholderTag(name="Student")
            teacher = StakeholderTag(name="Teacher")
            self_ = StakeholderTag(name="Self")
            parent = StakeholderTag(name="Parent")
            administrator = StakeholderTag(name="Administrator")

            student.save()
            teacher.save()
            self_.save()
            parent.save()
            administrator.save()
        
        if not InstitutionTag.objects.exists():
            # Create initial instances of MyModel
            primary = InstitutionTag(name = "Primary")
            secondary = InstitutionTag(name = "Secondary")
            tertiary = InstitutionTag(name = "Tertiary")

            primary.save()
            secondary.save()
            tertiary.save()