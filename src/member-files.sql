-- Member files: each Mason uploads to member-files/<their auth uid>/...; every signed-in member can open any file.
insert into storage.buckets (id, name, public, file_size_limit)
values ('member-files','member-files', false, 26214400)
on conflict (id) do update set public = false, file_size_limit = 26214400;

drop policy if exists "member files read" on storage.objects;
create policy "member files read" on storage.objects for select to authenticated
  using (bucket_id = 'member-files');

drop policy if exists "member files insert own" on storage.objects;
create policy "member files insert own" on storage.objects for insert to authenticated
  with check (bucket_id = 'member-files' and (storage.foldername(name))[1] = auth.uid()::text);

drop policy if exists "member files update own" on storage.objects;
create policy "member files update own" on storage.objects for update to authenticated
  using (bucket_id = 'member-files' and (storage.foldername(name))[1] = auth.uid()::text);

drop policy if exists "member files delete own" on storage.objects;
create policy "member files delete own" on storage.objects for delete to authenticated
  using (bucket_id = 'member-files' and (storage.foldername(name))[1] = auth.uid()::text);

select id, public, file_size_limit from storage.buckets where id = 'member-files';
