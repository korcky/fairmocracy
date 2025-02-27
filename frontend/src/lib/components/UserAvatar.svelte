<script>
    import { Avatar } from "@skeletonlabs/skeleton";
    let { userName = 'fallback', party = 'red' } = $props();
    let userInitials = Array.from(userName)[0];
    let partyBackground = party === 'blue' ? 'bg-blue-500' : party === 'red' ? 'bg-red-500' : 'bg-secondary-500' 
</script>

<Avatar initials={userInitials} background={partyBackground} width='w-32'/>